class VietOCRUtils:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model()