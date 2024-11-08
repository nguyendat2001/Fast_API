from PIL import Image
import cv2 

from utils.getEnvSetting import settings

class VietOCRUtils:
    def __init__(self):
        self.config_path = settings.ROOT_PATH + "/cfg/vietOCRConfig.json"
        self.config = self.loadConfig()
        self.predictor = self.loadPredictor()
    
    def loadConfig(self):
        from vietocr.tool.config import Cfg
        import json
        
        with open(self.config_path, 'r') as f:
            config_dict = json.load(f)
        
        modelConfig = config_dict.get("MODEL", {}).get("CONFIG", "vgg_transformer")
        modelWeight = config_dict.get("MODEL", {}).get("WEIGHT", "")
        device = config_dict.get("MODEL", {}).get("DEVICE", "cuda:0")
        modelPretrained = config_dict.get("MODEL", {}).get("CNN", {}).get("PRETRAINED", False)
        
        config = Cfg.load_config_from_name(modelConfig)
        if modelWeight and modelWeight.strip():  
            config['weights'] = modelWeight
        config['cnn']['pretrained'] = modelPretrained
        config['device'] = device
        print(config)
        return config
        
    def loadPredictor(self):
        from vietocr.tool.predictor import Predictor as VietOcr_Predictor
        return VietOcr_Predictor(self.config)
    
    def predict(self, imagePath):
        img = Image.open(imagePath)
        return self.predictor.predict(img, return_prob=True) # đối với muốn lấy trả về xác xuất dự đoán
    
    def predictImage(self, image):
        # img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        return self.predictor.predict(image, return_prob=True) # đối với muốn lấy trả về xác xuất dự đoán
    
