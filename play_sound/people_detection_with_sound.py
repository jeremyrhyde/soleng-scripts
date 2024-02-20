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
  
    # Get people_detector (vision service)
    people_detector = VisionClient.from_robot(robot, "people_detector")

    # Get sound_player (generic component)
    sound_player = Generic.from_robot(robot, "sound_player")

    # Start loop
    user_input = input("Press <Enter> to start: ")
    while True:
        if user_input == "Q":
            break

        people_detectors = await people_detector.get_detections_from_camera("webcam")
    
        for detection in people_detectors:
            if detection.class_name == "Person" and detection.confidence > 0.8:
                print(detection)
                sound_player_return_value = await sound_player.do_command({"message":"hello world"})
                print(f"sound_player do_command return value: {sound_player_return_value}") 

        time.sleep(1)


    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())