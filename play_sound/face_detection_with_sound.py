import asyncio
import time

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera 
from viam.components.generic import Generic
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='20cqh9adz7c6fkiih9ppbr1go0gr41y4',
      api_key_id='097504c3-1569-464a-bf81-53805bf93dae'
    )
    return await RobotClient.at_address('laptop-main.muhvcb3otx.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Get face_detector (vision service)
    face_detector = VisionClient.from_robot(robot, "face_detection")

    # Get sound_player (generic component)
    sound_player = Generic.from_robot(robot, "sound_player")

    # Start loop
    user_input = input("Press <Enter> to start: ")
    prev_face_detections = []
    while True:
        if user_input == "Q":
            break

        webcam_return_value = await webcam.get_image()
        face_detections = await face_detector.get_detections(webcam_return_value)
        #face_detections = await face_detector.get_detections_from_camera("webcam")
    
        new_face_detections = []
        for detection in face_detections:
            new_face_detections.append(detection.class_name)
            if detection.class_name == "jeremy" and "jeremy" not in prev_face_detections:
                sound_player_return_value = await sound_player.do_command({"message":"hello jeremy"})
                print(f"sound_player do_command return value: {sound_player_return_value}") 

            if detection.class_name == "bill" and "bill" not in prev_face_detections:
                sound_player_return_value = await sound_player.do_command({"message":"hello bill"})
                print(f"sound_player do_command return value: {sound_player_return_value}") 

        print("Detections: " + str(new_face_detections))
        prev_face_detections = new_face_detections

        time.sleep(1)


    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())