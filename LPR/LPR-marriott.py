import asyncio
import time
import json
import numpy as np
from io import BytesIO
from PIL import Image, ImageFilter
from datetime import datetime, timedelta
from typing import List
from viam.media.video import NamedImage, ViamImage
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera 
from viam.components.generic import Generic
from viam.services.vision import VisionClient, Detection


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='20cqh9adz7c6fkiih9ppbr1go0gr41y4',
        api_key_id='097504c3-1569-464a-bf81-53805bf93dae'
    )
    return await RobotClient.at_address('laptop-main.muhvcb3otx.viam.cloud', opts)

def get_best_detection(detections: List[Detection], label: str):
    max_confidence = 0.
    best_detection = None
    for detection in detections:
        if detection.confidence > max_confidence and (detection.x_max-detection.x_min)*(detection.y_max-detection.y_min) != 0 and detection.class_name == label:
            best_detection = detection
    return best_detection

def handle_license_plates(detection: Detection, image: Image):
    blur_image = image.crop((detection.x_min, detection.y_min, detection.x_max, detection.y_max)).filter(ImageFilter.GaussianBlur(radius=7))
    image.paste(blur_image,(detection.x_min,detection.y_min))
    return image

async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Recognize car & license plates
    car_detector = VisionClient.from_robot(robot, "car-detector")
    lpr_detector = VisionClient.from_robot(robot, "lpr-detector")

    # Start loop
    i = 0
    while True:
        try:
            # Get images
            for _ in range(0,3):
                await webcam.get_image()

            im = await webcam.get_image()
            detections = await car_detector.get_detections(im)     
            detection = get_best_detection(detections, "Car")
            # Check for detections
            if detection == None:
                continue

            image = Image.open(BytesIO(im.data))

            # Handle detection
            lpr_detections = await lpr_detector.get_detections(im)

            for detection in lpr_detections:
                image = handle_license_plates(detection, image)
            filename= "{}.jpg".format(datetime.now().isoformat('T'))
            image.save(filename)
            print("saving image: {}".format(filename))

            i = i + 1
            
            time.sleep(1)
        except Exception as e:
            print("Exception: " + str(e))

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())