import cv2
import numpy as np
import io


class Camera:
    def __init__(self, camera_id: int = 0, save_image_dir: str = '') -> None:
        self.cap = cv2.VideoCapture(camera_id)
        self.image_dir = save_image_dir


    def capture(self) -> np.ndarray:
        _, frame = self.cap.read()
        return frame


    def save_image(self, frame: np.ndarray, image_name: str):
        cv2.imwrite(f'{self.image_dir}/{image_name}', frame)


    @staticmethod
    def image_array_to_binary(image: np.ndarray, format: str = '.jpg') -> bytes:
        _, buffer = cv2.imencode('.jpg', image)
        io_buf = io.BytesIO(buffer)
        return io_buf.read()


if __name__ == '__main__':
    cat_cam = Camera('./test')
    frame = cat_cam.capture()
    cat_cam.save_image(frame, 'test.jpg')
