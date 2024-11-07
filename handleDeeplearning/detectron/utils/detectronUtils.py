import json
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog
from handleDeeplearning.vietocr.utils.vietOCRUils import VietOCRUtils

from handleDeeplearning.detectron.utils.dataHandle import registerMetaData

class DetectronUtil:
    def __init__(self, vietOCR):
        self.config_path = "/cfg/detectronConfig.json"
        self.config = self.loadConfig()
        self.predictor = self.loadPredictor()
        
        # Lấy metadata cho training dataset
        self.metaData = MetadataCatalog.get("test")
        self.classnames = self.metaData.thing_classes
        self.numclass = len(self.classnames)
        if vietOCR != null:
            self.ocrModel = vietOCR
        else :
            self.ocrModel = VietOCRUtils()
            
        
    def loadConfig(self):
        """Load Detectron2 config from a JSON file and configure the model settings."""
        # Đọc file JSON và chuyển thành dictionary
        with open(self.config_path, 'r') as f:
            config_dict = json.load(f)

        modelName = config_dict.get("MODEL", {}).get("NAME", "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        modelWeight = config_dict.get("MODEL", {}).get("WEIGHT", "/handleDeeplearning/detectron/weights/weights.pth")
        numClass = config_dict.get("MODEL", {}).get("NUMCLASSES", 12)
        scoreThresh = config_dict.get("MODEL", {}).get("ROI_HEADS", {}).get("SCORE_THRESH_TEST", 0.5)
        
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(modelName))
        cfg.MODEL.WEIGHTS = modelWeight  # Let training initialize from model zoo
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = numClass  # number of classes 
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = scoreThresh   # set a testing threshold
        return cfg

    def loadPredictor(self):
        """Load the Detectron2 model with the configuration."""
        from detectron2.engine import DefaultPredictor
        return DefaultPredictor(self.config)

    def processImagePath(self, image_path):
        """Read and preprocess the image for detection."""
        import cv2
        image = cv2.imread(image_path)
        return self.predictor(image)
    
    def processImage(self, image):
        """Read and preprocess the image for detection."""
        return self.predictor(image)

    def detectObjects(self, image_path):
        """Detect objects in the image."""
        outputs = self.processImagePath(image_path)
        instances = outputs["instances"].to("cpu")
        boxes = instances.pred_boxes if instances.has("pred_boxes") else None
        scores = instances.scores if instances.has("scores") else None
        classes = instances.pred_classes if instances.has("pred_classes") else None
        masks = instances.pred_masks if instances.has("pred_masks") else None # Lấy mask dự đoán
        
        return boxes, scores, classes, masks

    def getDetectedObjects(self, image_path):
        """Get bounding boxes, labels, and scores for detected objects."""
        boxes, scores, classes, masks = self.detectObjects(image_path)
        objects = []
        for i in range(len(classes)):
            obj = {
                "box": boxes[i].tensor.numpy().tolist(),
                "score": scores[i].item(),
                "class": MetadataCatalog.get(self.config.DATASETS.TRAIN[0]).thing_classes[classes[i]],
                "classId": MetadataCatalog.get(self.config.DATASETS.TRAIN[0]).thing_classes[classes[i]]
            }
            objects.append(obj)
        return objects
    
    def detectAC(self, imagePath):
        import cv2
        from PIL import Image
        
        im = cv2.imread(imagePath)
        boxes, scores, classes, masks = self.detectObjects(im);

        output_json = []
        for i in range(len(masks)):
            mask = masks[i].numpy()  # Chuyển mask sang numpy array
            box = boxes[i].tensor.numpy()[0]  # Chuyển bounding box sang numpy array
            class_id = classes[i].item()  # Lấy ID của class
            score = scores[i].item()  # Lấy confidence score
            
            # Lấy vùng chứa đối tượng từ bounding box
            x1, y1, x2, y2 = box.astype(int)
            cropped_image = im[y1:y2, x1:x2]  # Cắt ảnh dựa trên bounding box

            # Áp dụng mask để giữ lại chỉ vùng đối tượng trong bounding box
            masked_segment = cv2.bitwise_and(cropped_image, cropped_image, mask=mask[y1:y2, x1:x2].astype("uint8"))
            
            masked_segment_pil = Image.fromarray(cv2.cvtColor(masked_segment, cv2.COLOR_BGR2RGB))
            # using vietOCR to predict text
            text, text_score = self.ocrModel.predictImage(masked_segment_pil)
        #     print(masked_segment)
            output_json.append({
                "box": [int(x1), int(y1), int(x2), int(y2)],
                "text": text,
                "label_name": self.classnames[class_id],
                "label_id": class_id,
                "box_confidence_score": f"{score:.2f}" ,
                "text_confidence_score": f"{text_score:.2f}" 
            })
        return output_json
    
    def saveDetectedObjects(self, image_path, output_path):
        """Save the image with bounding boxes, labels, and scores."""
        import cv2
        from detectron2.utils.visualizer import Visualizer
        outputs = self.process_image(image_path)
        image = cv2.imread(image_path)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.config.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv2.imwrite(output_path, out.get_image()[:, :, ::-1])

