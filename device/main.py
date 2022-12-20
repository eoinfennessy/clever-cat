from dotenv import load_dotenv
import httpx
import os
from pocketbase import PocketBase
from camera import Camera
from dispenser import Dispenser
from feed_scheduler import FeedScheduler
from pet_detector import PetDetector


def update_feeder_config(event):
    pass

def update_feed_scheduler_config(event):
    pass

def setup():
    load_dotenv()
    pb = PocketBase(os.getenv('PB_URL'))

    # Authenticate user
    user_data = pb.collection('users').auth_with_password(
        os.getenv('PB_USER_EMAIL'), os.getenv('PB_USER_PASSWORD'))
    
    # Get feeder config from pb
    feeder_data = pb.collection('feeders').get_one(
        os.getenv('FEEDER_ID'), {'expand': 'model'})

    # Download feeder's model if not in models directory
    model_record = feeder_data.expand['model']
    if model_record.model not in os.listdir('./models'):
        model_url = pb.get_file_url(model_record, model_record.model, {})
        res = httpx.get(model_url)
        with open(f'./models/{model_record.model}', 'wb') as model:
            model.write(res.content)

    # Get detection labels - use generic 'cat' label if model's user is the default user
    if model_record.user == os.getenv('DEFAULT_USER_ID'):
        detection_labels = ['cat']
    else:
        detection_labels = model_record.pets

    # Initialise pet detector
    pet_detector = PetDetector(
        f'./models/{model_record.model}',
        detection_labels,
        confidence_threshold=0.5,
        max_results=1)

    # Initialise camera after making images directory
    if not os.path.exists('./images'):
        os.mkdir('./images')
    camera = Camera(camera_id=0, save_image_dir='./images')

    # Get feed schedules matching feeder ID
    feed_schedules = pb.collection('feed_schedules').get_full_list(1000, {'filter': f'feeder = "{os.getenv("FEEDER_ID")}"'})

    # Initialise feed schedulers after getting last dispensed feeds matching feeder ID and pets in feed schedules
    feed_schedulers = {}
    for feed_schedule in feed_schedules:
        last_feed = pb.collection('feeds').get_list(
            1, 1,
            {'filter': f'feeder = "{os.getenv("FEEDER_ID")}" && pet = "{feed_schedule.pet}"',
            'sort': '-created'})
        print(feed_schedule.pet, type(feed_schedule.pet))
        pet = pb.collection('pets').get_one(feed_schedule.pet)
        if pet.user == os.getenv('DEFAULT_USER_ID'):
            pet_key = 'cat'
        else:
            pet_key = feed_schedule.pet
        feed_schedulers[pet_key] = FeedScheduler(
            feed_schedule.amount_grams, feed_schedule.frequency_hours, last_feed[0].created)

    # Initialise dispenser
    dispenser = Dispenser(servo_pin=25, grams_per_second=3)

    # Set up subscription to feeder config using update_feeder_config callback
    pb.collection('feeders').subscribe(update_feeder_config)

    # Set up subscription to feed_scheduler using update_feed_scheduler_config callback
    pb.collection('feed_schedules').subscribe(update_feed_scheduler_config)

def main():
    # detections: list[dict[str, str | float]] = cat_cam.detect()
    # if detections: upload photo
    # for detection in detections:
    #     dispense_amount = feed_scheduler.amount_due(detection.label)
    #     if dispense_amount:
    #         dispenser.dispense(dispense_amount)
    #         Update feed table
    #         Update scheduler
    pass

if __name__ == '__main__':
    setup()