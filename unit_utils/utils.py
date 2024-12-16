import numpy as np

# def cell_text_localization(image):
#     cell_text_detector(image)
    
    
def convert_to_serializable(data):
    if isinstance(data, np.ndarray):
        return data.tolist()  # Chuyển ndarray sang list
    elif isinstance(data, (np.float32, np.float64)):
        return float(data)  # Chuyển float32 hoặc float64 sang float
    elif isinstance(data, (np.int32, np.int64)):
        return int(data)  # Chuyển int32 hoặc int64 sang int
    elif isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}  # Đệ quy xử lý dict
    elif isinstance(data, list):
        return [convert_to_serializable(v) for v in data]  # Đệ quy xử lý list
    else:
        return data  # Trả về dữ liệu gốc nếu đã serializable
