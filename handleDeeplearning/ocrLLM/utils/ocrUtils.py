from PIL import Image

def merge_images(image_paths):
    # Mở tất cả ảnh trong danh sách
    images = [Image.open(img_path) for img_path in image_paths]

    # Lấy kích thước của từng ảnh
    widths, heights = zip(*(img.size for img in images))

    # Đảm bảo tất cả ảnh có cùng chiều rộng
    max_width = max(widths)
    for i in range(len(images)):
        if images[i].width != max_width:
            images[i] = images[i].resize((max_width, int(images[i].height * (max_width / images[i].width))))

    # Tính toán kích thước ảnh mới
    combined_height = sum(img.height for img in images)
    new_image = Image.new('RGB', (max_width, combined_height))

    # Dán các ảnh vào ảnh mới theo thứ tự trong danh sách
    y_offset = 0
    for img in images:
        new_image.paste(img, (0, y_offset))
        y_offset += img.height

    return new_image  # Trả về ảnh đã được ghép