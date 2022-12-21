from dotenv import load_dotenv
from feeder import Feeder
import os

load_dotenv()

feeder = Feeder(
    os.getenv('PB_URL'),
    os.getenv('PB_USER_EMAIL'),
    os.getenv('PB_USER_PASSWORD'),
    os.getenv('FEEDER_ID'),
    os.getenv('DEFAULT_USER_ID'),
    './models'
)

while True:
    feeder.update()
