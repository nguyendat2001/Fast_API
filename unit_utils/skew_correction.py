import cv2
import numpy as np
import matplotlib.pyplot as plt

# customize delta=0.1, limit=10, display_steps=False
def correct_skew(image, delta=1, limit=5, display_steps=False):
    def determine_score(arr, angle):
        """Tính toán điểm số dựa trên độ nghiêng."""
        rotated = cv2.warpAffine(arr, cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0), (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=255)
        histogram = np.sum(rotated, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    if image is None:
        raise ValueError("Image could not be loaded. Check the file path.")

    # Bước 1: Xử lý ảnh thành nhị phân
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    # Cắt vùng ROI để giảm nhiễu (dựa trên contours lớn nhất)
    coords = np.column_stack(np.where(thresh > 0))
    x, y, w, h = cv2.boundingRect(coords)
    roi = thresh[y:y+h, x:x+w]

    # Bước 2: Phát hiện góc nghiêng
    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    h, w = roi.shape[:2]
    for angle in angles:
        _, score = determine_score(roi, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    # Bước 3: Hiệu chỉnh skew
    M = cv2.getRotationMatrix2D((w//2, h//2), best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]),
                               flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    if display_steps:
        # Hiển thị các bước xử lý
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.imshow(thresh, cmap='gray')
        plt.title("1. Binary Image")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.plot(angles, scores)
        plt.title("2. Angle Scores")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Score")

        plt.subplot(1, 3, 3)
        plt.imshow(corrected, cmap='gray')
        plt.title("3. Corrected Image")
        plt.axis("off")

        plt.tight_layout()
        plt.show()

    return best_angle, corrected

image = cv2.imread('/content/table.jpg')
angle, corrected = correct_skew(image)
print('Skew angle:', angle)

# Display the corrected image using matplotlib.pyplot
plt.imshow(cv2.cvtColor(corrected, cv2.COLOR_BGR2RGB)) # Convert to RGB for plt
plt.title('Corrected Image')
plt.axis('off') # Hide axes
plt.show()