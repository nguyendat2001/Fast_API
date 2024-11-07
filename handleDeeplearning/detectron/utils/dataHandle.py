import os, json
import cv2

from detectron2.structures import BoxMode
from detectron2.data import MetadataCatalog, DatasetCatalog

def registerMetaData(json_file_path):
    # Xóa tất cả dataset và metadata đã đăng ký trước đó
    DatasetCatalog.clear()
    MetadataCatalog.clear()

    # Đọc file JSON
    with open(json_file_path, 'r') as json_file:
        annotations = json.load(json_file)

    categories = annotations.get('categories', [])
    category_names = [category['name'] for category in categories]

    nc = len(category_names)
    names = category_names  # Giả sử category_names đã được định nghĩa trước đó
    d = "test"
    DatasetCatalog.register(d, lambda d=d: annotations)  # Đăng ký với chú thích tương ứng
    MetadataCatalog.get(d).set(thing_classes=names)

json_file_path = '/cfg/_annotations.coco.json'
registerMetaData(json_file_path)