from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

# ocr = PaddleOCR(use_angle_cls=True, lang='ml', det=True, rec=False, use_gpu=True,
#                det_db_box_thresh=0.2,  # Ngưỡng phát hiện hộp văn bản
#                 det_db_thresh=0.3      # Ngưỡng nhị phân hóa
#                )

def detect_image(ocr, image):
    import cv2
    import numpy as np
    
    results = ocr.ocr(image, cls=False)
    cropped_images = []
    for idx, line in enumerate(results[0]):
        # Lấy tọa độ box từ kết quả OCR
        box = line[0]  # 4 góc của bounding box

        # Chuyển đổi tọa độ sang dạng integer
        polygon = np.array(box, dtype=np.int32)

        # Tạo mặt nạ (mask) có cùng kích thước với ảnh gốc
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # Vẽ đa giác lên mặt nạ
        cv2.fillPoly(mask, [polygon], 255)

        # Cắt ảnh bằng cách áp dụng mặt nạ
        cropped = cv2.bitwise_and(image, image, mask=mask)

        # Lấy vùng chứa đa giác (bounding rectangle) để hiển thị vùng cắt
        x, y, w, h = cv2.boundingRect(polygon)
        cropped = cropped[y:y+h, x:x+w]
        cropped_images.append(cropped)
    return cropped_images

def detect_arrayimages(ocr, array_image):
    import cv2
    import numpy as np
    cropped_images = []
    for image in array_image:
        cropped_images += detect_image(image)
    return cropped_images