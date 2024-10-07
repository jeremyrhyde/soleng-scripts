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
from viam.components.sensor import Sensor 
from viam.components.camera import Camera 
from viam.components.generic import Generic
from viam.services.vision import VisionClient, Detection


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key="<API_KEY>",
        api_key_id="<API_KEY_ID>"
    )
    return await RobotClient.at_address('laptop-main.muhvcb3otx.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get webcam (camera component)
    intelrealsense_camera = Camera.from_robot(robot, "intelrealsense-cam")
    thermal_camera = Camera.from_robot(robot, "thermal-cam")
    tof_sensor = Sensor.from_robot(robot, "tof_sensor")

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