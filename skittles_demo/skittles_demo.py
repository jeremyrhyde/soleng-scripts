import asyncio
import time
import json

from PIL import Image 
from datetime import datetime, timedelta

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera 
from viam.components.motor import Motor 
from viam.components.generic import Generic
from viam.services.vision import VisionClient

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='fmpct6zudmdpohmu5rrni9f4no5ntp03',
        api_key_id='7a96d3a6-0ac1-49cb-b96c-7c0c37d39aa2'
    )
    return await RobotClient.at_address('skittles-demo-main.dxg9k7h3iq.viam.cloud', opts)

async def main():
    robot = await connect()

    # Open and load data file
    f = open("face-to-treat.json")
    treat_map = json.load(f)
    f.close()
    print("treat_map: ", str(treat_map))

    td = timedelta(seconds = 15)
    rpm = 40

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Get face_detector (vision service)
    face_detector = VisionClient.from_robot(robot, "detector")

    # Get sound_player (generic component)
    motor = Motor.from_robot(robot, "stepper")

    # Start loop
    input("Press <Enter> to start: ")
    prev_face_detections = {}
    while True:
        try:
            # Get image after clearing buffer
            for _ in range(0,3):
                await webcam.get_image()
            webcam_return_value = await webcam.get_image()

            # Return face detections from image
            face_detections = await face_detector.get_detections(webcam_return_value)
        
            if len(face_detections) == 0:
                print("No detections...")

            # Iterate through detections to determine which sound_byte to play
            for detection in face_detections:
                name = detection.class_name

                print("Detections: " + str(detection))

                # Skip people not in list
                if name not in treat_map.keys():
                    print("Skipping as name is not in treats list")
                    continue

                # Check if they already have gotten a treat in the last x time
                if name in prev_face_detections.keys():
                    now = datetime.now()
                    if now < prev_face_detections[name] + td:
                        print("Skipping as this person has recently had a snack")
                        continue

                # Add to list of known faces and actuate motor for desired time
                prev_face_detections[name] =  datetime.now()
                print("actuating motor... ({} rev)".format(treat_map[name]))
                await motor.go_for(rpm, treat_map[name])

            time.sleep(1)
        except Exception as e:
            print("Error: ", str(e))
            break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())