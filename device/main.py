from dotenv import load_dotenv
import httpx
import os
from pocketbase import PocketBase


def update_feeder_config():
    pass

def update_feed_schduler_config():
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

    # Initialise cat_cam

    # Get feed schedules matching feeder ID
    # Get last dispensed feeds matching pets in feed scheduler and feeder ID
    # Initialise feed_scheduler

    # Initialise dispenser

    # Set up subscription to feeder config using update_feeder_config callback
    # Set up subscription to feed_scheduler using update_feed_scheduler_config callback
    pass

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