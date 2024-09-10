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
        api_key='j5y6vgfybdd6n59swzmx1q7t4mkmme3q',
        api_key_id='e847a934-a29a-4495-a462-1e4de7b34909'
    )
    return await RobotClient.at_address('lpr-main.covge5vgpo.viam.cloud', opts)


async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "camera")

    # Recognize license plates
    lpr_detector = VisionClient.from_robot(robot, "vision-1")

    # Isolate text
    #ocr = VisionClient.from_robot(robot, "license-plates")

    # Start loop
    input("Press <Enter> to start: ")
    while True:
        try:
            for _ in range(0,3):
                await webcam.get_image()

            image = await webcam.get_image()
            lpr_detections = await lpr_detector.get_detections(image)
        
            # Iterate through LPR detections
            for detection in lpr_detections:
                print(detection)
                # if lpr_detection.confidence > .3 and lpr_detection.x_min != lpr_detection.x_max:
                #     print(lpr_detection)
                #     # Crop image using detected bounding box
                #     cropped_image = image.crop((lpr_detection.x_min, lpr_detection.y_min, 
                #                                lpr_detection.x_max, lpr_detection.y_max))
                    
                #     # Extract text from cropped image of licenses plate
                #     text_detections = await ocr.get_detections(cropped_image)

                #     license_plate = ""
                #     confidence_values = []
                #     for text_detection in text_detections:
                #         if text_detection.confidence > 50:
                #             license_plate = license_plate + text_detection.class_name
                #             confidence_values.append(text_detection.confidence)

                #     if license_plate != "":
                #         print("license_plate: " + license_plate + str(confidence_values))


            
            time.sleep(1)
        except Exception as e:
            print("Exception: " + str(e))
            break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())