import asyncio
import time
import csv 
from io import BytesIO
from PIL import Image
from datetime import datetime
from viam.robot.client import RobotClient
from viam.components.camera import Camera 


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key="<API_KEY>",
        api_key_id="<API_KEY_ID>"
    )
    return await RobotClient.at_address('realsensetest-main.unc6fit79p.viam.cloud', opts)


async def main():
    robot = await connect()

    # Get webcam (camera component)
    intelrealsense_camera = Camera.from_robot(robot, "intelrealsense-cam")

    # Clear buffer 
    for _ in range(0,3):
        await intelrealsense_camera.get_image()

    dir = "/home/ubuntu/data/realsense_camera/"

    # Start loop
    i = 0
    while True:
        try:
            (images, metadata) = await intelrealsense_camera.get_images()
            now = datetime.now()

            filename_jpg = dir + "rgb/{}.jpg".format(now.isoformat('T'))
            image = Image.open(BytesIO(images[0].data))
            image.save(filename_jpg)

            filename_pcd = dir + "pcd/{}.csv".format(now.isoformat('T'))
            with open(filename_pcd, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(images[1].bytes_to_depth_array())
            
            print("saving images: {} | {}".format(filename_jpg, filename_pcd))

            i = i + 1

            time.sleep(1)

        except Exception as e:
            print("Exception: " + str(e))

            if e == KeyboardInterrupt:
                break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())