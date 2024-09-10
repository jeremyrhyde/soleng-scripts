import asyncio
from datetime import datetime
from viam.robot.client import RobotClient
from viam.components.camera import Camera 


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='2r9c7hpk97qik8i7aolst70yur1nkd0n',
        api_key_id='0cc9c563-1dc8-4553-9bf7-f4c6ae8d71ad'
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
            with open(filename_jpg, "wb") as file:
                file.write(images[0].data)

            filename_pcd = dir + "pcd/{}.pcd".format(now.isoformat('T'))
            with open(filename_pcd, "wb") as file:
                file.write(images[1].data)
            
            
            print("saving images: {} | {}".format(filename_jpg, filename_pcd))

            i = i + 1

        except Exception as e:
            print("Exception: " + str(e))

            if e == KeyboardInterrupt:
                break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())