import json
import cv2
import numpy as np
from PIL import Image
import os
import time

from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
import nest_asyncio
nest_asyncio.apply()
from llama_index.core.llms import ChatMessage

from handleDeeplearning.ocrLLM.prompts import hos108, hos110, hosTamAnh, idCard
from handleDeeplearning.ocrLLM.utils.ocrUtils import *


llm_json = Ollama(model="llama3.2", request_timeout=120.0
             , json_mode=True
             )

class Unit_OCR():
    def __init__(self, llm, prompt_parser,llama_Index_key):
        self.llm = llm
        self.prompt_parser = prompt_parser
        self.llama_Index_key = llama_Index_key
        self.praser  = LlamaParse(
            api_key=llama_Index_key,
            result_type="markdown",  # "markdown" and "text" are available
            language="vi",
            premium_mode=True,
            # page_separator=""
            do_not_unroll_columns=True,
            is_formatting_instruction=True,
            # parsing_instruction=prompt_parser
        )
        self.system_prompt = "bạn là chuyên gia trong trích xuất thông tin dưới dạng json. hãy trả lại thông tin dưới dạng json format. trả lời đúng trọng tâm không cần cầu kì."


    def scan_detection(self, image):
      global document_contour
      document_contour = np.array([[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])

      # Chuyển ảnh sang ảnh xám và làm mờ để giảm nhiễu
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      blur = cv2.GaussianBlur(gray, (5, 5), 0)

      # Áp dụng phương pháp nhị phân hóa ảnh (Otsu's thresholding)
      _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

      # Tìm tất cả các contours
      contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

      # Sắp xếp các contours theo diện tích
      contours = sorted(contours, key=cv2.contourArea, reverse=True)

      max_area = 0
      for contour in contours:
          area = cv2.contourArea(contour)
          if area > 1000:  # Chỉ quan tâm đến những contours có diện tích lớn hơn ngưỡng
              peri = cv2.arcLength(contour, True)
              approx = cv2.approxPolyDP(contour, 0.015 * peri, True)

              # Nếu đường bao có diện tích lớn nhất và có 4 đỉnh
              if area > max_area and len(approx) == 4:
                  document_contour = approx
                  max_area = area

      # Kiểm tra nếu tìm được document_contour có 4 đỉnh
      if len(document_contour) == 4:
          # Sắp xếp các điểm theo thứ tự (trái trên, phải trên, phải dưới, trái dưới)
          pts = document_contour.reshape(4, 2)
          rect = np.zeros((4, 2), dtype="float32")

          s = pts.sum(axis=1)
          rect[0] = pts[np.argmin(s)]
          rect[2] = pts[np.argmax(s)]

          diff = np.diff(pts, axis=1)
          rect[1] = pts[np.argmin(diff)]
          rect[3] = pts[np.argmax(diff)]

          # Xác định kích thước tài liệu
          (tl, tr, br, bl) = rect
          widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
          widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
          maxWidth = max(int(widthA), int(widthB))

          heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
          heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
          maxHeight = max(int(heightA), int(heightB))

          # Điểm đích cho hình ảnh được biến đổi
          dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")

          # Phép biến đổi phối cảnh
          M = cv2.getPerspectiveTransform(rect, dst)
          warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

          return warp

      # Trường hợp không tìm thấy document_contour
      return image

    def inference_scan(self, imgLs):
        outdir = "/content/output_scan/"
        # Kiểm tra xem có tồn tại thư mục và tạo sau đó scan từng image và lưu lại trong file này
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        processed_images = []

        for img_path in imgLs:
            # Đọc ảnh và thực hiện quét
            image = cv2.imread(img_path)
            scanned_image = self.scan_detection(image)

            # Lưu ảnh đã quét vào thư mục
            base_name = os.path.basename(img_path)
            output_path = os.path.join(outdir, f"scanned_{base_name}")
            cv2.imwrite(output_path, scanned_image)
            print(f"image {base_name} has been scan")
            # Thêm đường dẫn ảnh đã quét vào danh sách
            processed_images.append(output_path)

        return processed_images
    def init_prompt_template_tam_anh(self, content):
      # Replace context
      return hosTamAnh.prompt.format(context=content)

    def init_prompt_template_IDCARD(self, content):
      # Replace context
      return idCard.prompt.format(context=content)

    def init_prompt_template_110_hos(self, content):
      # Replace context
      return hos110.prompt.format(context=content)

    def init_prompt_template_108_hos(self, content):
      return hos108.prompt.format(context=content)

    def send_message(self,template):
      print("start predict")
      messages = [
          ChatMessage(
              # role="system", content="dựa vào thông tin markdown bênh dưới hãy truy xuất dưới dạng json"
              role="system", content=self.system_prompt
          ),
          ChatMessage(role="user", content=template),
      ]
      resp = llm_json.chat(messages)
      print(" predict complete")
      return resp

    def get_context(self, imgLs):
      _, file_extension = os.path.splitext(imgLs[0])
      file_extractor = {file_extension: self.praser} # Replace parser with self.praser
      result = SimpleDirectoryReader(input_files=imgLs, file_extractor=file_extractor,recursive=True)
      documents = result.load_data()

      text = ""
      for doc in documents:
        text += doc.text

      table = []
      content = ""
      for item in text.split("\n"):
          if item.startswith('|'):  # Corrected the syntax error here
              table = item.split('\n')
          else:
              content += item + '\n\n'
      if len(table) > 1:
          table.remove(table[1])

      table = [[y.strip() for y in x.split('|')[1:-1]] for x in table]
      return content, table

    def merge_images_to_array(self, imgLs):
      new_LS = []
      merge_flag = True;
      if merge_flag:
        tmp = 0
        while tmp < len(imgLs):
            if len(imgLs)%2 != 0 and tmp + 1 >= len(imgLs):
                new_LS = new_LS[:tmp] + [imgLs[-1]]
                break
            elif len(imgLs)%2 != 0 and tmp + 1 >= len(imgLs):
                break
            
            merged_img = merge_images([imgLs[tmp], imgLs[tmp + 1]])
            
            if merged_img is not None:
                outputPath = f"/content/combined_{tmp//2}.jpg" 
                
                # Convert the PIL Image to a NumPy array
                merged_img_np = np.array(merged_img) 
                
                # Write the NumPy array to file using cv2.imwrite
                cv2.imwrite(outputPath, merged_img_np) 
                
                new_LS = new_LS[:tmp] + [outputPath]
            tmp += 2
      return new_LS

    def inference(self, template, table):
      resp = self.send_message(template)
      json_resp = json.loads(resp.message.content)
      json_resp['table_content'] = table
      return json_resp

    def inferenceIdCard(self, imgPath):
      _, file_extension = os.path.splitext(imgPath)
      file_extractor = {file_extension: self.praser} # Replace parser with self.praser
      result = SimpleDirectoryReader(input_files=[
          imgPath],file_extractor=file_extractor,recursive=True)
      documents = result.load_data()

      text = ""
      for doc in documents:
        text += doc.text
      # print("text :"+text)
      template = self.init_prompt_template_IDCARD(text)
      resp = self.send_message(template)
      json_resp = json.loads(resp.message.content)
      return json_resp

    def inferenceHos110(self, imgPath):
      _, file_extension = os.path.splitext(imgPath[0])
      file_extractor = {file_extension: self.praser} # Replace parser with self.praser
      result = SimpleDirectoryReader(input_files=imgPath, file_extractor=file_extractor,recursive=True)
      documents = result.load_data()

      text = ""
      for doc in documents:
        text += doc.text
      table = []
      endTableFlag = False
      content = ""
      for item in text.split("\n"):
          if "đơn vị tính" in item.lower() or "nội dung" in item.lower() or "(12)" in item.lower() or "(13)" in item.lower() or "--" in item.lower() or "quỹ bhyt" in item.lower():
              continue
          if item.startswith('|') and not endTableFlag:  # Kiểm tra nếu dòng bắt đầu bằng '|'
              table.append(item)  # Thêm dòng vào danh sách table
          else:
              content += item + '\n\n'  # Thêm dòng vào content với hai dấu xuống dòng
          if "cộng:" in item.lower():  # Kiểm tra nếu dòng chứa từ "Cộng:"
              endTableFlag = True  # Đánh dấu flag kết thúc bảng
      table = [[y.strip() for y in x.split('|')[1:-1]] for x in table]
      template = self.init_prompt_template_108_hos(content)
      resp = self.send_message(template)
      json_resp = json.loads(resp.message.content)
      json_resp["table_content"] = table
      return json_resp

    def inferenceHosTamAnh(self, imgPath):
      imgPath = self.merge_images_to_array(imgPath)

      _, file_extension = os.path.splitext(imgPath[0])
      file_extractor = {file_extension: self.praser} # Replace parser with self.praser
      result = SimpleDirectoryReader(input_files=imgPath, file_extractor=file_extractor,recursive=True)
      documents = result.load_data()

      text = ""
      for doc in documents:
        text += doc.text
      table = []
      endTableFlag = False
      content = ""
      for item in text.split("\n"):
          if "tổng chi phí" in item.lower():  # Kiểm tra nếu dòng chứa từ "Cộng:"
              endTableFlag = True  # Đánh dấu flag kết thúc bảng

          if item.startswith('|') and not endTableFlag:  # Kiểm tra nếu dòng bắt đầu bằng '|'
              table.append(item)  # Thêm dòng vào danh sách table
          else:
              content += item + '\n\n'  # Thêm dòng vào content với hai dấu xuống dòng

      table = [[y.strip() for y in x.split('|')[1:-1]] for x in table]
      template = self.init_prompt_template_tam_anh(content)
      resp = self.send_message(template)
      json_resp = json.loads(resp.message.content)
      json_resp["table_content"] = table
      return json_resp

