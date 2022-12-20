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


if __name__ == '__main__':
    # model_path = './model/lite-model_ssd_mobilenet_v1_1_metadata_2.tflite' # 0.73, 0.49 sec
    # model_path = './model/lite-model_efficientdet_lite4_detection_metadata_2.tflite' # 0.75 - Extremely slow
    # model_path = './model/lite-model_object_detection_mobile_object_localizer_v1_1_metadata_2.tflite' # No labels?
    # model_path = './model/lite-model_efficientdet_lite0_detection_metadata_1.tflite' # 0.65, 0.97 sec
    model_path = './model/lite-model_efficientdet_lite1_detection_metadata_1.tflite' # 0.84, 1.78 sec
    # model_path = './model/lite-model_efficientdet_lite2_detection_metadata_1.tflite' # 0.77, 2.75 sec
    # model_path = './model/lite-model_yolo-v5-tflite_tflite_model_1.tflite' # Didn't immediately work
    image_path = './images/cat.jpeg'

    # Initialization
    base_options = core.BaseOptions(file_name=model_path)
    detection_options = processor.DetectionOptions(
        max_results=2,
        category_name_allowlist=['cat'],
        score_threshold=0.4
        )
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Run inference
    start = time.time()

    image = vision.TensorImage.create_from_file(image_path)

    detection_result = detector.detect(image)

    total_time = time.time() - start

    print(detection_result)
    print('Total time: ', total_time)