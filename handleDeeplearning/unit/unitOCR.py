from handleDeeplearning.detectron.utils.dataHandle import registerMetaData
from handleDeeplearning.unit.utils import  ( initDetectronPredictor, 
                                            BOUNDING_BOX_EXTRACTION, 
                                            get_cropped_images_by_classnames_with_metadata, 
                                            detect_and_sort_crops, 
                                            get_texts_from_unmerge_image)
from detectron2.data import MetadataCatalog, DatasetCatalog

class unitOCR():
    def __init__(self, vietOCR, text_detection_anotation, doc_structure_anotation, table_cell_anotation):
        if vietOCR is not None: 
            self.vietOCR = vietOCR
        else:
            self.vietOCR = VietOCRUtils()
        
        name_text_detection = "text_detection"
        registerMetaData(text_detection_anotation, name_text_detection)
        self.metaData_text_detection = MetadataCatalog.get(name_text_detection)


        name_doc_structure = "doc_structure"
        registerMetaData(doc_structure_anotation, name_doc_structure)
        self.metaData_doc_structure = MetadataCatalog.get(name_doc_structure)

        name_table_cell = "table_cell"
        registerMetaData(table_cell_anotation, name_table_cell)
        self.metaData_table_cell = MetadataCatalog.get(name_table_cell)
        
        self.config_path = os.path.join(config_path if config_path else "cfg/unit/", "main.json")

        # Đọc file JSON và chuyển thành dictionary
        with open(self.config_path, 'r') as f:
            config_dict = json.load(f)

        text_detector_score_thresh = config_dict.get("MODEL", {}).get("TEXT_DETECTION", {}).get("SCORE_THRESH_TEST", 0.5)
        doc_structure_detector_score_thresh = config_dict.get("MODEL", {}).get("CELL_TEXT_DETECTION", {}).get("SCORE_THRESH_TEST", 0.5)
        table_cell_detector_score_thresh = config_dict.get("MODEL", {}).get("DOC_STRUCTURE_DETECTION", {}).get("SCORE_THRESH_TEST", 0.5)
        
        text_detector_weight = config_dict.get("MODEL", {}).get("TEXT_DETECTION", {}).get("WEIGHT")
        doc_structure_detector_weight = config_dict.get("MODEL", {}).get("CELL_TEXT_DETECTION", {}).get("WEIGHT")
        table_cell_detector_weight = config_dict.get("MODEL", {}).get("DOC_STRUCTURE_DETECTION", {}).get("WEIGHT")
        
        text_detector_model = config_dict.get("MODEL", {}).get("TEXT_DETECTION", {}).get("MODEL")
        doc_structure_detector_model = config_dict.get("MODEL", {}).get("CELL_TEXT_DETECTION", {}).get("MODEL")
        table_cell_detector_model = config_dict.get("MODEL", {}).get("DOC_STRUCTURE_DETECTION", {}).get("MODEL")
        
        self.text_detector = initDetectronPredictor(text_detector_weight, text_detector_model, text_detector_score_thresh, self.metaData_text_detection)
        self.doc_structure_detector = initDetectronPredictor(doc_structure_detector_weight, doc_structure_detector_model, doc_structure_detector_score_thresh, self.metaData_doc_structure)
        self.table_cell_detector = initDetectronPredictor(table_cell_detector_weight, table_cell_detector_model, table_cell_detector_score_thresh, self.metaData_table_cell)
    

    def predict(self, image_arrays):
        header_text = []
        sumary_text = []
        table_raw_data = []
        for item in image_arrays:
            im = cv2.imread(item)
            # outputs = BOUNDING_BOX_EXTRACTION(im, doc_structure_detector,metaData_doc_structure)
            
            outputs, _, _, _, _ = BOUNDING_BOX_EXTRACTION(im, self.doc_structure_detector, self.metaData_doc_structure, True)
            
            classname = ["item"]
            row_images = get_cropped_images_by_classnames_with_metadata(im, outputs, classname, self.metaData_doc_structure)
            
            classname = ["text_box","sub_head_box"]
            head_text_images = get_cropped_images_by_classnames_with_metadata(im, outputs, classname, self.metaData_doc_structure)

            classname = ["sumary"]
            sumary_text_images = get_cropped_images_by_classnames_with_metadata(im, outputs, classname, self.metaData_doc_structure)
            
            table_raw_data += table_infor_extraction(row_images, table_cell_detector, self.vietOCR)
            
            # get text from header, sumary and sub_head_box
            sorted_text_crops = detect_and_sort_crops(head_text_images, text_detector, 20)
            head_array_texts = get_texts_from_unmerge_image(sorted_text_crops, self.vietOCR)

            sorted_text_crops = detect_and_sort_crops(sumary_text_images, text_detector, 20)
            sumary_array_texts = get_texts_from_unmerge_image(sorted_text_crops, self.vietOCR)

        return header_text, sumary_text, table_raw_data
    
    