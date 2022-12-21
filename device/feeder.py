import datetime
import httpx
import json
import os
from pocketbase import PocketBase
from pocketbase.client import FileUpload, Record
from camera import Camera
from dispenser import Dispenser
from feed_scheduler import FeedScheduler
from pet_detector import PetDetector


class Feeder:
    def __init__(self, pocketbase_url: str, user_email: str, user_password: str,
                 feeder_id: str, default_user_id: str, model_dir: str) -> None:
        self.model_dir = model_dir
        self.default_user_id = default_user_id
        self.pb = PocketBase(pocketbase_url)
        self.user_data = self.pb.collection('users').auth_with_password(
            user_email, user_password
        )
        self.default_pet_id = self.pb.collection('pets').get_list(
            1, 1, {'filter': f'user = "{default_user_id}"'}
        ).items[0].id
        self.camera = Camera(camera_id=0)
        self.dispenser = Dispenser(servo_pin=25, grams_per_second=3)
        self.feeder_record: Record
        self.model_record: Record
        self.pet_detector: PetDetector
        self.feed_schedulers: dict[str, FeedScheduler]

        self.set_feeder_record(self.pb.collection('feeders').get_one(feeder_id))

        self.set_model_record(
            self.pb.collection('models').get_one(self.feeder_record.model)
        )
        self.download_model_if_not_exists()

        self.update_pet_detector()

        self.set_feed_schedulers(
            self.pb.collection('feed_schedules').get_full_list(
                1000, {'filter': f'feeder = "{feeder_id}"'}
            )
        )

        # Set up subscriptions
        self.pb.collection('feeders').subscribe(self.handle_feeders_events)
        self.pb.collection('feed_schedules').subscribe(self.handle_feed_schedules_events)


    def set_feeder_record(self, feeder_record: Record) -> None:
        self.feeder_record = feeder_record

    
    def set_model_record(self, model_record: Record) -> None:
        self.model_record = model_record


    def download_model_if_not_exists(self):
        if self.model_record.model not in os.listdir(self.model_dir):
            model_url = self.pb.get_file_url(self.model_record, self.model_record.model, {})
            res = httpx.get(model_url)
            with open(f'{self.model_dir}/{self.model_record.model}', 'wb') as model:
                model.write(res.content)


    def update_pet_detector(self):
        # Get detection labels - use generic 'cat' label if model's user is the default user
        detection_labels = ['cat'] if self.model_record.user == self.default_user_id else self.model_record.pets

        self.pet_detector = PetDetector(
            f'{self.model_dir}/{self.model_record.model}',
            detection_labels,
            confidence_threshold=0.5,
            max_results=1)


    def set_feed_schedulers(self, feed_schedules):
        schedulers = {}
        for feed_schedule in feed_schedules:
            last_feed = self.pb.collection('feeds').get_list(
                1, 1,
                {'filter': f'feeder = "{self.feeder_record.id}" && pet = "{feed_schedule.pet}"',
                'sort': '-created'}
            )
            if last_feed.items:
                last_feed_time = last_feed.items[0].created
            else:
                last_feed_time = datetime.datetime(1970, 1, 1, 0, 0)

            schedulers[feed_schedule.pet] = FeedScheduler(
                feed_schedule.amount_grams, feed_schedule.frequency_hours, last_feed_time
            )
        self.feed_schedulers = schedulers


    @staticmethod
    def convert_bounding_box(bounding_box):
        bounds = {}
        bounds['min_x'] = bounding_box.origin_x
        bounds['min_y'] = bounding_box.origin_y
        bounds['max_x'] = bounds['min_x'] + bounding_box.width
        bounds['max_y'] = bounds['min_y'] + bounding_box.height
        return bounds

    
    def handle_feeders_events(self, event):
        pass


    def handle_feed_schedules_events(self, event):
        pass


    def update(self):
        image = self.camera.capture()
        result = self.pet_detector.detect_from_array(image)

        # TODO: Separate pet_photos entity into photos and detections
        if result.detections:
            image_binary = Camera.image_array_to_binary(image, '.jpg')
        for detection in result.detections:
            pet = detection.categories[0].category_name
            if pet == 'cat':
                pet = self.default_pet_id

            bounding_box = self.convert_bounding_box(detection.bounding_box)

            # Upload photo and photo reccord
            pet_photo_record = self.pb.collection('pet_photos').create({
                'user': self.user_data.record.id,
                'pet': pet,
                'photo': FileUpload((f'{pet}.jpg', image_binary)),
                'bounding_box': json.dumps(bounding_box),
                'confidence': detection.categories[0].score,
                'feeder': self.feeder_record.id
            })

            feed_amount = self.feed_schedulers[pet].get_feed_amount_due()
            if feed_amount:
                self.dispenser.dispense(feed_amount)

                feed = self.pb.collection('feeds').create({
                    'feeder': self.feeder_record.id,
                    'pet': pet,
                    'photo': pet_photo_record.id,
                    'grams_dispensed': feed_amount
                })

                self.feed_schedulers[pet].time_of_last_feed = feed.created
