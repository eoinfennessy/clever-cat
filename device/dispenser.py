from gpiozero import Servo
import time


class Dispenser:
    def __init__(self, servo_pin: int, grams_per_second: float = 5) -> None:
        self.servo = Servo(servo_pin)
        self.grams_per_second = grams_per_second
        pass


    def dispense(self, grams: float) -> None:
        self.servo.max()
        time.sleep((1 / self.grams_per_second) * grams)
        self.servo.min()


if __name__ == '__main__':
    feeder = Dispenser(servo_pin=25, grams_per_second=1)
    feeder.dispense(grams=0.5)
