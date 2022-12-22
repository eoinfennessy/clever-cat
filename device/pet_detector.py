import numpy as np
from tflite_support.task import core, processor, vision
import time


class PetDetector:
    def __init__(self,
                 model_path: str,
                 labels_to_detect: list[str]=['cat'],
                 confidence_threshold: float=0.4,
                 max_results: int=2
                 ) -> None:
        self.model_path = model_path
        self.labels_to_detect = labels_to_detect
        self.confidence_threshold = confidence_threshold
        self.max_results = max_results
        self.detector = self._initialise_detector()


    def _initialise_detector(self) -> vision.ObjectDetector:
        base_options = core.BaseOptions(file_name=self.model_path)
        detection_options = processor.DetectionOptions(
            max_results=self.max_results,
            category_name_allowlist=self.labels_to_detect,
            score_threshold=self.confidence_threshold
            )
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            detection_options=detection_options
            )
        return vision.ObjectDetector.create_from_options(options)


    def detect_from_file(self, image_path: str) -> processor.DetectionResult:
        image = vision.TensorImage.create_from_file(image_path)
        return self.detector.detect(image)

        
    def detect_from_array(self, image_array: np.ndarray) -> processor.DetectionResult:
        image = vision.TensorImage.create_from_array(image_array)
        return self.detector.detect(image)
