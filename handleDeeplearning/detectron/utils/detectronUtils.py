import json
from detectron2.config import get_cfg

def registerDataset(name, img_dir, json_file):
    DatasetCatalog.register(name, lambda: get_data_dicts(img_dir))
    MetadataCatalog.get(name).set(thing_classes=category_names)

DatasetCatalog.clear()
MetadataCatalog.clear()
register_dataset("test", "/kaggle/input/cccd-detection/test", "_annotations.coco.json")

class DetectronUtil:
    def __init__(self):
        self.config_path = "/cfg/detectronConfig.json"
        self.config = self.load_config()
        self.model = self.load_model()

    def getMetaData(self):
        
        
        self.register_dataset("test", "/kaggle/input/cccd-detection/test", "_annotations.coco.json")
        return MetadataCatalog.get("test")
    
        
    def loadConfig(self):
        """Load Detectron2 config from a JSON file and configure the model settings."""
        cfg = get_cfg()

        # Đọc file JSON và chuyển thành dictionary
        with open(self.config_path, 'r') as f:
            config_dict = json.load(f)

        # Merge dictionary với cấu hình Detectron2
        cfg.merge_from_list(self.convert_dict_to_cfg(config_dict))

        # Thiết lập các giá trị mặc định cho một số tham số, ví dụ: DEVICE và ngưỡng SCORE_THRESH_TEST
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = config_dict.get("MODEL", {}).get("ROI_HEADS", {}).get("SCORE_THRESH_TEST", 0.5)
        cfg.MODEL.DEVICE = config_dict.get("MODEL", {}).get("DEVICE", "cpu")
        return cfg

    def convertDictToCfg(self, config_dict):
        """Convert the dictionary into a list format suitable for `merge_from_list`."""
        cfg_list = []
        for key, value in config_dict.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    cfg_list.append(f"{key}.{sub_key}")
                    cfg_list.append(sub_value)
            else:
                cfg_list.append(key)
                cfg_list.append(value)
        return cfg_list

    def loadModel(self):
        """Load the Detectron2 model with the configuration."""
        from detectron2.engine import DefaultPredictor
        return DefaultPredictor(self.config)

    def processImage(self, image_path):
        """Read and preprocess the image for detection."""
        import cv2
        image = cv2.imread(image_path)
        outputs = self.model(image)
        return outputs

    def detectObjects(self, image_path):
        """Detect objects in the image."""
        outputs = self.process_image(image_path)
        instances = outputs["instances"].to("cpu")
        boxes = instances.pred_boxes if instances.has("pred_boxes") else None
        scores = instances.scores if instances.has("scores") else None
        classes = instances.pred_classes if instances.has("pred_classes") else None
        return boxes, scores, classes

    def getDetectedObjects(self, image_path):
        """Get bounding boxes, labels, and scores for detected objects."""
        boxes, scores, classes = self.detect_objects(image_path)
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

    def saveDetectedObjects(self, image_path, output_path):
        """Save the image with bounding boxes, labels, and scores."""
        import cv2
        from detectron2.utils.visualizer import Visualizer
        outputs = self.process_image(image_path)
        image = cv2.imread(image_path)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.config.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        cv2.imwrite(output_path, out.get_image()[:, :, ::-1])

