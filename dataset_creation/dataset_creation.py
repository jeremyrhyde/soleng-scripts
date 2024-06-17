import asyncio

from datetime import datetime

from viam.robot.client import RobotClient
from viam.components.camera import Camera 

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

    # throw out a few initial images
    for _ in range(0,3):
        await webcam.get_image()

    while True:
        cmd = input("Press Enter to take a picture, Q to quit: ")
        if cmd == "Q" or cmd == "q":
            break
        try:
            image = await webcam.get_image()
            time = datetime.now()
            timestamp = time.isoformat('T')
            timestamp_filename = timestamp.replace(":","_") + ".png"

            # Save image with timestamp
            image.save("/Users/jeremyhyde/.viam/capture/rdk_component_camera/webcam/" + timestamp_filename)
                
        except:
            continue

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())