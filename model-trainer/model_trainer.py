import os
import uuid
import shutil
import httpx
import random
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from pocketbase import PocketBase
from pocketbase.models import Record
from tflite_model_maker import model_spec, object_detector

load_dotenv()

app = FastAPI()

pb = PocketBase(os.getenv('POCKETBASE_URL'))
pb.admins.auth_with_password(
    os.getenv('POCKETBASE_ADMIN_EMAIL'), os.getenv('POCKETBASE_ADMIN_PASSWORD')
    )

model_specification = model_spec.get('efficientdet_lite0')

def create_data_dir() -> str:
    working_dir = str(uuid.uuid4())
    os.mkdir(working_dir)
    return working_dir

def get_photo_records(pet_id: str) -> list[Record]:
    return pb.collection('pet_photos').get_full_list(10000, {filter: f'pet = {pet_id}'})

def download_photo(photo_url: str, filename: str) -> None:
    res = httpx.get(photo_url)
    with open(filename, 'wb') as photo:
        photo.write(res.content)

def append_to_csv(csv_filename: str, split_designation: str, photo_filename: str, pet_id: str, bounding_box: dict[str, float]) -> None:
    with open(csv_filename, 'a') as pet_photos:
        pet_photos.write(
            f'{split_designation},{photo_filename},{pet_id},{bounding_box["x1"]},{bounding_box["y1"]},,,{bounding_box["x2"]},{bounding_box["y2"]},,\n'
        )

def train():
    pass

def upload_model():
    pass

@app.post('/model_trainer/')
def train_model(pet_ids: list[str]):
    data_dir = create_data_dir()

    for pet_id in pet_ids:
        photo_records = get_photo_records(pet_id)
        for photo_record in photo_records:
            photo_url = pb.get_file_url(photo_record, photo_record.photo, {})
            photo_path = f'{data_dir}/{photo_record.photo}'

            download_photo(photo_url, photo_path)
            split_designation = random.choices(('TRAINING', 'VALIDATION', 'TEST'), weights=(8, 1, 1))
            append_to_csv(f'{data_dir}/pet_photos.csv', split_designation, photo_path, pet_id, photo_record.bounding_box)

    train_data, validation_data, test_data = object_detector.DataLoader.from_csv(f'./{data_dir}/pet_photos.csv')
    model = object_detector.create(train_data, model_spec=model_specification, batch_size=8, train_whole_model=True, validation_data=validation_data)
    model.evaluate(test_data)
    model.export(export_dir=f'./{data_dir}')
    model.evaluate_tflite(f'./{data_dir}/model.tflite', test_data)
