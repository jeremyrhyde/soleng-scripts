import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.camera import Camera 
from viam.components.base import Base
from viam.services.vision import VisionClient

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='ig8r23hpv7527lsyxn28u51be0fvfjzb',
        api_key_id='23b76826-ba96-4a3d-aaeb-b59ddaa1f3ac'
    )
    return await RobotClient.at_address('rover-0-main.b2fkxt2kv3.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Get face_detector (vision service)
    face_detector = VisionClient.from_robot(robot, "face-detection")

    # Get rover (base component)
    rover = Base.from_robot(robot, "viam_base")

    rotational_speed = 50
    translational_speed = 50

    # Start loop
    input("Press <Enter> to start: ")
    while True:
        try:
            for _ in range(0,3):
                await webcam.get_image()

            image = await webcam.get_image()
            face_detections = await face_detector.get_detections(image)
        
            # Iterate through detections to determine which sound_byte to play
            print("Detections: ")
            for detection in face_detections:
                print("- {}".format(detection.class_name))

                # Handle detections of 'jeremy'
                if detection.class_name == "jeremy":
                    await rover.spin(720, rotational_speed) 

                # Handle detections of 'hazal'
                if detection.class_name == "hazal":
                    await rover.move_straight(25, translational_speed)
                    await rover.spin(90, rotational_speed)
                    await rover.spin(-90, rotational_speed)
                    await rover.move_straight(-25, translational_speed)

                # -----------------------------------
                # ADD DETECTION OF NEW PERSON

                # -----------------------------------
                
            time.sleep(1)
        except:
            continue

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())