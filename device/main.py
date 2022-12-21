import datetime
from dotenv import load_dotenv
import httpx
import json
import os
from pocketbase import PocketBase
from pocketbase.client import FileUpload
from camera import Camera
from dispenser import Dispenser
from feed_scheduler import FeedScheduler
from pet_detector import PetDetector


def update_feeder_config(event):
    pass

def update_feed_scheduler_config(event):
    pass

def convert_bounding_box(bounding_box):
    bounds = {}
    bounds['min_x'] = bounding_box.origin_x
    bounds['min_y'] = bounding_box.origin_y
    bounds['max_x'] = bounds['min_x'] + bounding_box.width
    bounds['max_y'] = bounds['min_y'] + bounding_box.height
    return bounds

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
    last_feed_time = last_feed.items[0].created if last_feed.items else datetime.datetime(1970, 1, 1, 0, 0)

    feed_schedulers[feed_schedule.pet] = FeedScheduler(
        feed_schedule.amount_grams, feed_schedule.frequency_hours, last_feed_time)

# Initialise dispenser
dispenser = Dispenser(servo_pin=25, grams_per_second=3)

# Set up subscription to feeder config using update_feeder_config callback
pb.collection('feeders').subscribe(update_feeder_config)

# Set up subscription to feed_scheduler using update_feed_scheduler_config callback
pb.collection('feed_schedules').subscribe(update_feed_scheduler_config)


while True:
    image = camera.capture()
    result = pet_detector.detect_from_array(image)
    print(result)

    # TODO: Separate pet_photos entity into photos and detections
    if result.detections:
        # Convert image
        image_bin = Camera.image_array_to_binary(image, '.jpg')
    for detection in result.detections:
        pet = detection.categories[0].category_name
        if pet == 'cat':
            pet = 'quur5oezlmz4vi8'

        bounding_box = convert_bounding_box(detection.bounding_box)

        # Upload photo and photo reccord
        pet_photo_record = pb.collection('pet_photos').create({
            'user': 'nl3lfndpbytt7pe',
            'pet': pet,
            'photo': FileUpload((f'{pet}.jpg', image_bin)),
            'bounding_box': json.dumps(bounding_box),
            'confidence': detection.categories[0].score,
            'feeder': os.getenv('FEEDER_ID')
            })

        feed_amount = feed_schedulers[pet].get_feed_amount_due()
        if feed_amount:
            dispenser.dispense(feed_amount)

            feed = pb.collection('feeds').create({
                'feeder': os.getenv('FEEDER_ID'),
                'pet': pet,
                'photo': pet_photo_record.id,
                'grams_dispensed': feed_amount
            })

            feed_schedulers[pet].time_of_last_feed = feed.created

    # detections: list[dict[str, str | float]] = cat_cam.detect()
    # if detections: upload photo
    # for detection in detections:
    #     dispense_amount = feed_scheduler.amount_due(detection.label)
    #     if dispense_amount:
    #         dispenser.dispense(dispense_amount)
    #         Update feed table
    #         Update scheduler


# if __name__ == '__main__':
#     setup()