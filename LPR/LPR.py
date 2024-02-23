import asyncio
import time
import json

from PIL import Image 
from datetime import datetime, timedelta

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera 
from viam.components.generic import Generic
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='9dk9w3pz4pxayyzsgdb39k3rlnmxbvrh',
      api_key_id='c3c37e2e-5a8b-4826-9f06-e05d01d54bb9'
    )
    return await RobotClient.at_address('laptop-alt-main.muhvcb3otx.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Recognize license plates
    lpr_detector = VisionClient.from_robot(robot, "LPR-detector")

    # Isolate text
    ocr = VisionClient.from_robot(robot, "license-plates")

    # Start loop
    input("Press <Enter> to start: ")
    while True:
        try:
            for _ in range(0,3):
                await webcam.get_image()

            image = await webcam.get_image()
            lpr_detections = await lpr_detector.get_detections(image)
        
            # Iterate through LPR detections
            for lpr_detection in lpr_detections:
                if lpr_detection.confidence > 0.3:

                    # Crop image using detected bounding box
                    cropped_image = image.crop((lpr_detection.x_min, lpr_detection.y_min, 
                                               lpr_detection.x_max, lpr_detection.y_max))
                    
                    # Extract text from cropped image of licenses plate
                    text_detections = await ocr.get_detections(cropped_image)

                    license_plate = ""
                    confidence_values = []
                    for text_detection in text_detections:
                        if text_detection.confidence > 50:
                            license_plate = license_plate + text_detection.class_name
                            confidence_values.append(text_detection.confidence)

                    if license_plate != "":
                        print("license_plate: " + license_plate + str(confidence_values))


            
            time.sleep(1)
        except Exception as e:
            print("Exception: " + str(e))
            break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())