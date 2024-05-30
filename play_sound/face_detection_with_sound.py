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

async def connectrover():
    opts = RobotClient.Options.with_api_key(
      api_key='20cqh9adz7c6fkiih9ppbr1go0gr41y4',
      api_key_id='097504c3-1569-464a-bf81-53805bf93dae'
    )
    return await RobotClient.at_address('laptop-main.muhvcb3otx.viam.cloud', opts)


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='20cqh9adz7c6fkiih9ppbr1go0gr41y4',
      api_key_id='097504c3-1569-464a-bf81-53805bf93dae'
    )
    return await RobotClient.at_address('laptop-main.muhvcb3otx.viam.cloud', opts)

async def main():
    robot = await connect()
    roverrobot = await connectrover()
    # Open and load data file
    f = open("face-to-hello.json")
    sound_map = json.load(f)
    f.close()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Get face_detector (vision service)
    face_detector = VisionClient.from_robot(robot, "face-detector")

    # Get sound_player (generic component)
    sound_player = Generic.from_robot(roverrobot, "sound_player")

    # Start loop
    input("Press <Enter> to start: ")
    prev_face_detections = []
    while True:
        try:
            for _ in range(0,3):
                await webcam.get_image()

            init_time = datetime.now()
            webcam_return_value = await webcam.get_image()
            print(datetime.now()-init_time)
            face_detections = await face_detector.get_detections(webcam_return_value)
            print(datetime.now()-init_time)
            #face_detections = await face_detector.get_detections_from_camera("webcam")
        
            # Iterate through detections to determine which sound_byte to play
            new_face_detections = []
            for detection in face_detections:
                name = detection.class_name
                if name in sound_map.keys():
                    new_face_detections.append(name)
                    if name not in prev_face_detections:
                        await sound_player.do_command({sound_map[name]["type"]:sound_map[name]["sound_byte"]})

            print("Detections: " + str(new_face_detections))
            prev_face_detections = new_face_detections
            
            time.sleep(1)
        except:
            break

    # Don't forget to close the machine when you're done!
    await sound_player.do_command({"stop":""})
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())