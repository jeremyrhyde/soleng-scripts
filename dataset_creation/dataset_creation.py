import asyncio
import io

from datetime import datetime
from PIL import Image

from viam.robot.client import RobotClient
from viam.components.camera import Camera 

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='tfpk14dibqm2197nur4cwii2xokqob6u',
        api_key_id='500e242d-e560-4eac-8156-fcbd4af0dd7a'
    )
    return await RobotClient.at_address('laptop-new-main.muhvcb3otx.viam.cloud', opts)


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
            vimage = await webcam.get_image()
            time = datetime.now()
            timestamp = time.isoformat('T')
            timestamp_filename = timestamp.replace(":","_") + ".png"

            # Save image with timestamp
            image = Image.open(io.BytesIO(vimage.data))
            image.save("/Users/jeremyhyde/.viam/capture/rdk_component_camera/webcam/" + timestamp_filename)
                
        except Exception as e:
            print(e)
            continue

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())