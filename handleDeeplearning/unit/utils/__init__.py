
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# common libraries
import numpy as np
import os, json, cv2, random
import matplotlib.pyplot as plt
from PIL import Image
# %matplotlib inline

# detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
from detectron2.utils.visualizer import ColorMode

def get_data_dicts(img_dir):
    """
    Get dataset dictionaries in the format required by Detectron2 for training.
    """
    # Đường dẫn đến file chú thích COCO
    json_file_path = os.path.join(img_dir, "_annotations.coco.json")
    dataset_dicts = []
    
    # Đọc file JSON
    with open(json_file_path, 'r') as json_file:
        annotations = json.load(json_file)

    # Duyệt qua danh sách các hình ảnh từ annotations
    for img_info in annotations['images']:
        record = {}
        
        # Đường dẫn đến file hình ảnh
        filename = os.path.join(img_dir, img_info['file_name'])
        
        # Đọc hình ảnh
        img = cv2.imread(filename)
        
        if img is None:
            print(f"Warning: {filename} could not be read.")
            continue
        
        height, width = img.shape[:2]
        
        # Thêm thông tin về hình ảnh vào record
        record["file_name"] = filename
        record["image_id"] = img_info['id']
        record["height"] = height
        record["width"] = width
        objs = []
        
        # Duyệt qua các chú thích
        for annotation in annotations['annotations']:
            if annotation['image_id'] == img_info['id']:
                label = annotation['category_id']
                segmentation = annotation['segmentation']
                
                # Tạo đối tượng chứa segmentation và category_id
                obj = {
                    "segmentation": segmentation,
                    "bbox": annotation['bbox'],  # Giả định bbox đã có sẵn
                    "bbox_mode": BoxMode.XYWH_ABS,
                    "category_id": label,
                }
                objs.append(obj)
        
        record["annotations"] = objs
        dataset_dicts.append(record)
    
    return dataset_dicts

def initDetectronPredictor(model_id, weight_path, thresh_score, meta_data):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(model_id))
#     cfg.DATALOADER.NUM_WORKERS = 1
#     os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    cfg.MODEL.WEIGHTS = os.path.join(weight_path) # path to the model we trained

    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = thresh_score # set a testing threshold
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(meta_data.thing_classes)  # number of classes 
    return DefaultPredictor(cfg)

def GET_PREDICT_BOX(outputs):
    instances = outputs["instances"]
    boxes = instances.pred_boxes.tensor.cpu().numpy()  # Bounding boxes
    scores = instances.scores.cpu().numpy()  # Điểm số
    classes = instances.pred_classes.cpu().numpy()  # Nhãn (class IDs)

    # Kết hợp bounding boxes và vùng cắt ảnh
    cropped_images_with_boxes = []
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)  # Lấy tọa độ bounding box
        cropped = im[y1:y2, x1:x2]  # Cắt vùng dự đoán từ ảnh
        cropped_images_with_boxes.append({"cropped": cropped, "y1": y1})

    # Sắp xếp vùng cắt dựa trên `y1` (tọa độ trên cùng của box)
    cropped_images_with_boxes_sorted = sorted(
        cropped_images_with_boxes, key=lambda x: x["y1"]
    )

    # Lấy danh sách vùng cắt sau khi sắp xếp
    cropped_images_sorted = [item["cropped"] for item in cropped_images_with_boxes_sorted]

    # Chuyển thành NumPy array
    cropped_images_array = np.array(cropped_images_sorted, dtype=object)  # dtype=object vì kích thước khác nhau

    return cropped_images_array

# text detection function
def detect_and_crop_sorted_by_y(predictor, image, metadata):
    """
    Sử dụng mô hình Detectron2 để dự đoán, crop các bounding box từ ảnh và sắp xếp theo trục y.

    Args:
        predictor (DefaultPredictor): Predictor được tạo từ Detectron2.
        image (ndarray): Ảnh đầu vào (numpy array).
        metadata (Metadata): Metadata chứa thông tin về các class.

    Returns:
        list: Danh sách các ảnh crop, sắp xếp theo tọa độ y_min.
    """
    # Thực hiện dự đoán
    outputs = predictor(image)

    # Lấy thông tin từ kết quả dự đoán
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Bounding boxes
    scores = instances.scores.numpy()  # Confidence scores
    classes = instances.pred_classes.numpy()  # Class IDs

    # Lưu thông tin box và ảnh crop
    cropped_images_with_boxes = []
    for i in range(len(boxes)):
        x_min, y_min, x_max, y_max = boxes[i].astype(int)
        cropped_image = image[y_min:y_max, x_min:x_max]  # Crop ảnh
        cropped_images_with_boxes.append({
            "cropped_image": cropped_image,
            "box": (x_min, y_min, x_max, y_max)
        })

    # Sắp xếp các ảnh crop theo y_min
    # cropped_images_with_boxes = sorted(cropped_images_with_boxes, key=lambda r: r["box"][1])
    cropped_images_with_boxes = sorted(cropped_images_with_boxes, key=lambda b: b["box"][0])
    # Trả về danh sách các ảnh crop
    cropped_images = [item["cropped_image"] for item in cropped_images_with_boxes]

    return cropped_images

def crop_and_sort_boxes(im, outputs, target_classes):
    """
    Crop các box theo class IDs chỉ định và sắp xếp theo tọa độ.

    Args:
        im (ndarray): Ảnh gốc.
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.
        target_classes (list): Danh sách các class ID cần crop.

    Returns:
        list: Danh sách các mảng ảnh crop đã được sắp xếp.
    """
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Lấy bounding boxes
    classes = instances.pred_classes.numpy()  # Lấy class IDs

    # Lọc các box thuộc target_classes
    cropped_boxes = []
    for i, class_id in enumerate(classes):
        if class_id in target_classes:
            x_min, y_min, x_max, y_max = boxes[i].astype(int)
            cropped_boxes.append({
                "class_id": class_id,
                "box": (x_min, y_min, x_max, y_max),
                "image": im[y_min:y_max, x_min:x_max]
            })

    # Phân loại theo class_id
    sorted_boxes = {
        "text_and_subhead": [],
        "sumary": []
    }

    for box in cropped_boxes:
        if box["class_id"] == 5:  # sumary
            sorted_boxes["sumary"].append(box)
        else:  # text_box hoặc sub_head_box
            sorted_boxes["text_and_subhead"].append(box)

    # Sắp xếp text_box và sub_head_box theo y_min, sau đó x_min
    sorted_boxes["text_and_subhead"].sort(
        key=lambda b: (b["box"][1], b["box"][0])
    )

    # Kết hợp lại, sumary ở cuối
    final_sorted = (
        sorted_boxes["text_and_subhead"] + sorted_boxes["sumary"]
    )

    # Trả về danh sách ảnh đã được crop
    return [box["image"] for box in final_sorted]

def group_text_to_cells(outputs):
    """
    Nhóm các text vào các cell dựa trên quan hệ không gian (bounding boxes),
    và sắp xếp cell theo trục x_min. Index của cell_to_texts được gán lại để khớp với thứ tự hiển thị.

    Args:
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.

    Returns:
        tuple: 
            - cell_to_texts (dict): Dictionary ánh xạ từ index (sau khi sắp xếp) tới danh sách ID của text.
            - ungrouped_texts (list): Danh sách ID của text không thuộc cell nào.
            - cell_confidences (list): Danh sách độ tin cậy (confidence) của các cell theo thứ tự sắp xếp.
    """
    # Lấy thông tin bounding box, nhãn và score từ outputs
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Bounding boxes
    labels = instances.pred_classes.numpy()      # Labels (0: cell, 1: text)
    scores = instances.scores.numpy()            # Confidence scores

    # Tách bounding boxes và scores theo loại
    cells = []  # List các bounding box của cell
    texts = []  # List các bounding box và ID của text
    confidences = []  # List confidence score của cell
    for i, label in enumerate(labels):
        if label == 0:  # Cell
            cells.append(boxes[i])  # Chỉ lấy bounding box
            confidences.append(scores[i])  # Lưu confidence score
        elif label == 1:  # Text
            texts.append((boxes[i], i))  # Gắn ID để tham chiếu

    # Sắp xếp các cell theo trục x_min
    sorted_cells_with_confidence = sorted(
        zip(cells, confidences), key=lambda x: x[0][0]  # Sắp xếp dựa trên x_min của cell
    )

    # Tách bounding boxes và scores đã sắp xếp
    sorted_cells = [item[0] for item in sorted_cells_with_confidence]
    cell_confidences = [item[1] for item in sorted_cells_with_confidence]

    # Tạo dictionary ánh xạ từ thứ tự mới của cell
    cell_to_texts = {new_idx: [] for new_idx in range(len(sorted_cells))}

    # Nhóm text vào cell
    ungrouped_texts = []  # Text không thuộc cell nào
    for text_box, text_id in texts:
        assigned = False
        for new_idx, cell_box in enumerate(sorted_cells):
            # Kiểm tra nếu text_box nằm trong cell_box
            if is_box_inside(text_box, cell_box):
                cell_to_texts[new_idx].append(text_id)
                assigned = True
                break
        if not assigned:
            ungrouped_texts.append(text_id)

    return cell_to_texts, ungrouped_texts, cell_confidences

def is_box_inside(box1, box2):
    """
    Kiểm tra nếu trung tâm của bounding box1 nằm trong bounding box2.
    box: [x_min, y_min, x_max, y_max]

    Args:
        box1 (list): Tọa độ của bounding box1 [x_min, y_min, x_max, y_max].
        box2 (list): Tọa độ của bounding box2 [x_min, y_min, x_max, y_max].

    Returns:
        bool: True nếu trung tâm của box1 nằm trong box2, False nếu không.
    """
    # Tính tọa độ trung tâm của box1
    center_x = (box1[0] + box1[2]) / 2
    center_y = (box1[1] + box1[3]) / 2

    # Kiểm tra trung tâm có nằm trong box2 không
    return (
        box2[0] <= center_x <= box2[2] and  # Trung tâm x nằm trong giới hạn x của box2
        box2[1] <= center_y <= box2[3]      # Trung tâm y nằm trong giới hạn y của box2
    )


def crop_text_images(im, outputs, cell_to_texts):
    """
    Crop các text images từ ảnh gốc dựa trên cell_to_texts.
    
    Args:
        im (ndarray): Ảnh gốc (numpy array).
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.
        cell_to_texts (dict): Dictionary nhóm text ID theo cell ID.
    
    Returns:
        dict: Dictionary chứa danh sách các text images được crop, theo cell ID.
    """
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Lấy bounding boxes
    labels = instances.pred_classes.numpy()      # Lấy labels (0: cell, 1: text)

    cropped_texts = {}  # Lưu các text images theo cell
    for cell_id, text_ids in cell_to_texts.items():
        cropped_texts[cell_id] = []  # Mỗi cell là một danh sách text images
        for text_id in text_ids:
            # Lấy bounding box của text
            x_min, y_min, x_max, y_max = boxes[text_id].astype(int)
            # Crop ảnh
            text_crop = im[y_min:y_max, x_min:x_max]
            cropped_texts[cell_id].append(text_crop)

    return cropped_texts

def get_cropped_texts_by_cell(cell_id, im, outputs, cell_to_texts):
    """
    Trả về các ảnh text đã được crop từ cell ID, và sắp xếp theo trục y (từ trên xuống dưới).

    Args:
        cell_id (int): ID của cell cần lấy các text.
        im (ndarray): Ảnh gốc (numpy array).
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.
        cell_to_texts (dict): Dictionary nhóm text ID theo cell ID.

    Returns:
        list: Danh sách mảng ảnh đã được crop từ các text thuộc cell ID, sắp xếp theo trục y.
    """
    # Kiểm tra cell_id có tồn tại trong cell_to_texts
    if cell_id not in cell_to_texts:
        raise ValueError(f"Cell ID {cell_id} không tồn tại trong cell_to_texts.")

    # Lấy danh sách text IDs thuộc cell
    text_ids = cell_to_texts[cell_id]

    # Lấy bounding boxes và crop ảnh
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Lấy bounding boxes

    cropped_boxes = []
    for text_id in text_ids:
        # Lấy bounding box của text
        x_min, y_min, x_max, y_max = boxes[text_id].astype(int)
        # Crop ảnh từ ảnh gốc
        cropped_image = im[y_min:y_max, x_min:x_max]
        cropped_boxes.append({
            "box": (x_min, y_min, x_max, y_max),
            "cropped_image": cropped_image
        })

    # Sắp xếp các box theo y_min (từ trên xuống) và x_min (nếu cần để phân biệt các box có y_min giống nhau)
    cropped_boxes_sorted = sorted(cropped_boxes, key=lambda b: (b["box"][1], b["box"][0]))

    # Trích xuất các ảnh đã được crop từ danh sách sắp xếp
    cropped_images = [b["cropped_image"] for b in cropped_boxes_sorted]

    return cropped_images

def BOUNDING_BOX_EXTRACTION(im, predictor, metaData, is_plot_img:True):
    """
    Hàm vẽ bounding boxes, nhóm text theo cell và crop text images.
    """
    # Chạy dự đoán
    outputs = predictor(im)
    
    # Nhóm text theo cell
    cell_to_texts, ungrouped_texts, confidents = group_text_to_cells(outputs)

    # Crop text images
    cropped_texts = crop_text_images(im, outputs, cell_to_texts)
    if is_plot_img:
        # Hiển thị hình ảnh với dự đoán
        visualizer = Visualizer(im[:, :, ::-1], metadata=metaData, scale=0.5, instance_mode=ColorMode.IMAGE_BW)
        predict = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
        predict_image = predict.get_image()[:, :, ::-1]
    
        plt.figure(figsize=(20, 20))
        plt.imshow(predict_image)
        plt.show()

    # Trả về outputs và các kết quả
    return outputs, cell_to_texts, ungrouped_texts, cropped_texts, confidents

def get_cropped_images_by_classnames_with_metadata(im, outputs, classnames, metadata, delta_y=10):
    """
    Lấy danh sách các ảnh crop theo nhiều class name, sử dụng metadata,
    và sắp xếp theo thứ tự từ trên xuống và trái sang phải (dựa trên trung điểm).

    Args:
        im (ndarray): Ảnh gốc (numpy array).
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.
        classnames (list): Danh sách tên các class cần crop.
        metadata (Metadata): Metadata của mô hình Detectron2.

    Returns:
        list: Danh sách các ảnh đã được crop, sắp xếp theo thứ tự từ trên xuống.
    """
    # Kiểm tra các classnames có tồn tại trong metadata không
    invalid_classes = [classname for classname in classnames if classname not in metadata.thing_classes]
    if invalid_classes:
        raise ValueError(f"Các class không tồn tại trong metadata: {invalid_classes}")

    # Lấy ID của tất cả các class trong danh sách
    class_ids = [metadata.thing_classes.index(classname) for classname in classnames]

    # Lấy thông tin từ outputs
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Lấy bounding boxes
    classes = instances.pred_classes.numpy()  # Lấy class IDs

    # Lọc box có class_id tương ứng và tính trung điểm
    cropped_boxes = []
    for i, pred_class_id in enumerate(classes):
        if pred_class_id in class_ids:
            x_min, y_min, x_max, y_max = boxes[i].astype(int)
            x_mid = (x_min + x_max) // 2
            y_mid = (y_min + y_max) // 2
            cropped_boxes.append({
                "box": (x_min, y_min, x_max, y_max),
                "cropped_image": im[y_min:y_max, x_min:x_max],
                "x_mid": x_mid,
                "y_mid": y_mid
            })

    # Sắp xếp theo y_mid trước và x_mid sau (với y cho phép chênh lệch 10px)
    cropped_boxes = sorted(
        cropped_boxes,
        key=lambda b: (b["y_mid"] // delta_y, b["x_mid"])  # Chia y_mid theo nhóm khoảng cách 10px
    )

    # Trích xuất các ảnh đã được crop từ danh sách sắp xếp
    cropped_images = [b["cropped_image"] for b in cropped_boxes]

    return cropped_images

def get_cropped_images_by_classnames_with_metadata_sort_x(im, outputs, classnames, metadata):
    """
    Lấy danh sách các ảnh crop theo nhiều class name, sử dụng metadata,
    và sắp xếp theo thứ tự từ trên xuống và trái sang phải.

    Args:
        im (ndarray): Ảnh gốc (numpy array).
        outputs (dict): Kết quả dự đoán từ mô hình Detectron2.
        classnames (list): Danh sách tên các class cần crop.
        metadata (Metadata): Metadata của mô hình Detectron2.

    Returns:
        list: Danh sách các ảnh đã được crop, sắp xếp theo thứ tự từ trên xuống.
    """
    # Kiểm tra các classnames có tồn tại trong metadata không
    invalid_classes = [classname for classname in classnames if classname not in metadata.thing_classes]
    if invalid_classes:
        raise ValueError(f"Các class không tồn tại trong metadata: {invalid_classes}")

    # Lấy ID của tất cả các class trong danh sách
    class_ids = [metadata.thing_classes.index(classname) for classname in classnames]

    # Lấy thông tin từ outputs
    instances = outputs["instances"].to("cpu")
    boxes = instances.pred_boxes.tensor.numpy()  # Lấy bounding boxes
    classes = instances.pred_classes.numpy()  # Lấy class IDs

    # Lọc box có class_id tương ứng
    cropped_boxes = []
    for i, pred_class_id in enumerate(classes):
        if pred_class_id in class_ids:
            x_min, y_min, x_max, y_max = boxes[i].astype(int)
            cropped_boxes.append({
                "box": (x_min, y_min, x_max, y_max),
                "cropped_image": im[y_min:y_max, x_min:x_max]
            })

    # Sắp xếp các box theo y_min (trên xuống) và x_min (trái sang phải)
    cropped_boxes = sorted(cropped_boxes, key=lambda b: b["box"][0])

    # Trích xuất các ảnh đã được crop từ danh sách sắp xếp
    cropped_images = [b["cropped_image"] for b in cropped_boxes]

    return cropped_images

def detect_and_sort_crops(cropped_images, text_detector, delta_y=10):
    """
    Dự đoán các bounding boxes trong từng ảnh crop, 
    sắp xếp theo trục y trước và x khi y chênh lệch nhỏ hơn ngưỡng delta_y.

    Args:
        cropped_images (list): Danh sách các mảng ảnh (numpy array) đã được crop.
        text_detector (DefaultPredictor): Mô hình Detectron2 đã được khởi tạo để phát hiện text.
        delta_y (int): Ngưỡng chênh lệch trục y để quyết định thứ tự.

    Returns:
        list: Danh sách các mảng ảnh đã được sắp xếp.
    """
    all_sorted_crops = []

    # Lặp qua từng crop (giữ thứ tự index)
    for index, crop in enumerate(cropped_images):
        # Dự đoán trên từng ảnh crop
        outputs = text_detector(crop)
        instances = outputs["instances"].to("cpu")

        # Lấy thông tin bounding boxes
        boxes = instances.pred_boxes.tensor.numpy()

        # Lưu thông tin bounding boxes và ảnh crop tương ứng
        sorted_crops = []
        for box in boxes:
            x_min, y_min, x_max, y_max = box.astype(int)
            center_x = (x_min + x_max) / 2  # Trung điểm x
            center_y = (y_min + y_max) / 2  # Trung điểm y
            sorted_crops.append({
                "box": (x_min, y_min, x_max, y_max),
                "center": (center_x, center_y),  # Tọa độ trung điểm
                "cropped_image": crop[y_min:y_max, x_min:x_max],
                "image_index": index  # Thứ tự index của ảnh gốc
            })

        # Sắp xếp các box trong crop theo trung điểm y trước, trung điểm x sau
        sorted_crops = sorted(
            sorted_crops,
            key=lambda item: (item["center"][1] // delta_y, item["center"][0])
        )
        all_sorted_crops.extend(sorted_crops)

    # Sắp xếp toàn bộ danh sách theo index của cropped_images
    all_sorted_crops = sorted(all_sorted_crops, key=lambda item: item["image_index"])

    # Trích xuất ảnh đã được sắp xếp
    final_sorted_images = [item["cropped_image"] for item in all_sorted_crops]

    return final_sorted_images

def get_raw_text(cell_images, row_im, outputs, cell_to_texts, confidents, viet_ocr):
    raw_text = []
    for index, item in enumerate(cell_images):
        array_text = get_cropped_texts_by_cell(index, row_im, outputs, cell_to_texts)
        text, score = get_texts_from_cell_merge_images(array_text, viet_ocr, True)
        # raw_text.append({"confident": confidents[index],
        #                  "text":text})
        raw_text.append({
            "cell": {
                # "confident": confidents[index],
                "confident": score,
                "text": text
            }
        })

    return raw_text

def get_raw_text_by_paddle_ocr(cell_images, paddle_ocr, confidents, viet_ocr):
    """
    Nhận diện văn bản từ danh sách ảnh và trả về danh sách kết quả.

    Args:
        cell_images (list): Danh sách ảnh (numpy array).
        paddle_ocr (PaddleOCR): Đối tượng PaddleOCR.
        confidents (list): Danh sách độ tin cậy ban đầu.
        viet_ocr: Đối tượng OCR tiếng Việt.
    
    Returns:
        list: Danh sách chứa thông tin văn bản và độ tin cậy.
    """
    from handleDeeplearning.paddle_ocr import detect_image
    
    raw_text = []  # Danh sách chứa kết quả cuối cùng
    
    for index, item in enumerate(cell_images):
        # Phát hiện văn bản từ ảnh
        array_text = detect_image(paddle_ocr, item)
        
        # Xử lý khi không phát hiện được văn bản
        if len(array_text) == 0:
            text, score = "", 1.0  # Giá trị mặc định
        else:
            # Trích xuất văn bản và độ tin cậy
            text, score = get_texts_from_cell_merge_images(array_text, viet_ocr, True)
        
        # Thêm kết quả vào danh sách
        raw_text.append({
            "cell": {
                "confident": score,
                "text": text
            }
        })
    
    # In số lượng kết quả
    print(f"raw_text: {len(raw_text)}")
    
    return raw_text

def table_infor_extraction(row_images, table_cell_detector, viet_ocr, metaData_table_cell):
    table_data = []
    for row_im in row_images:
        outputs, cell_to_texts, abc , _, confidents = BOUNDING_BOX_EXTRACTION(row_im, table_cell_detector, metaData_table_cell, False)
        
        classname = ["cell"]
        cell_images = get_cropped_images_by_classnames_with_metadata_sort_x(row_im, outputs, classname, metaData_table_cell)

        raw_text = get_raw_text(cell_images, row_im, outputs, cell_to_texts, confidents, viet_ocr)
        table_data.append(raw_text)
    return table_data

def get_texts_from_cell_merge_images(cropped_texts, viet_ocr, return_prob=True):
    """
    Dự đoán đoạn văn bản từ các ảnh text đã crop, sau khi nối ảnh từ trái sang phải.

    Args:
        cropped_texts (list): Danh sách các mảng ảnh (numpy arrays) đã được crop.
        viet_ocr (VietOcr_Predictor): Mô hình ViệtOCR đã được khởi tạo.

    Returns:
        str: Đoạn văn bản dự đoán từ ảnh đã nối.
    """
    if not cropped_texts:
        if return_prob:
            return "", 1.0  # Trả về văn bản rỗng và xác suất 1.0
        else:
            return ""  # Trả về văn bản rỗng

    # Lấy chiều cao lớn nhất trong các ảnh (tránh thực hiện nhiều vòng lặp)
    max_height = max(img.shape[0] for img in cropped_texts)

    # Resize và nối các ảnh lại bằng numpy
    resized_texts = [
        cv2.resize(img, (int(img.shape[1] * max_height / img.shape[0]), max_height), interpolation=cv2.INTER_LINEAR)
        for img in cropped_texts
    ]
    combined_image = np.concatenate(resized_texts, axis=1)  # Nối theo chiều ngang

    # Dự đoán văn bản trực tiếp từ numpy array
    pil_image = Image.fromarray(cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB))  # Đổi BGR thành RGB
    return viet_ocr.predict(pil_image, return_prob)



def get_texts_from_unmerge_image(cropped_texts, viet_ocr, batch_size=16, return_prob=True):
    """
    Dự đoán đoạn văn bản từ các ảnh text đã crop theo batch.

    Args:
        cropped_texts (list): Danh sách các mảng ảnh (numpy arrays) đã được crop.
        viet_ocr (VietOcr_Predictor): Mô hình ViệtOCR đã được khởi tạo.
        batch_size (int): Số lượng ảnh xử lý trong mỗi batch.

    Returns:
        list: Danh sách các đoạn văn bản dự đoán từ từng ảnh.
    """
    if not cropped_texts:
        if return_prob:
            return [],[]
        else: 
            return []

    # Chuyển đổi ảnh numpy sang định dạng PIL Image
    pil_images = [Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) for img in cropped_texts]
    return viet_ocr.predict_batch(pil_images, return_prob)

def table_infor_extraction_by_paddle_ocr(row_images, paddle_ocr, table_cell_detector, viet_ocr, metaData_table_cell):
    table_data = []
    for row_im in row_images:
        outputs, cell_to_texts, abc , _, confidents = BOUNDING_BOX_EXTRACTION(row_im, table_cell_detector, metaData_table_cell, False)
        
        classname = ["cell"]
        cell_images = get_cropped_images_by_classnames_with_metadata_sort_x(row_im, outputs, classname, metaData_table_cell)

        raw_text = get_raw_text_by_paddle_ocr(cell_images, paddle_ocr, confidents, viet_ocr)
        table_data.append(raw_text)
    return table_data