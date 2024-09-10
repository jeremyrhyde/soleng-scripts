import asyncio
from datetime import datetime
from viam.robot.client import RobotClient
from viam.components.camera import Camera 


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='7kb0piio6bnuh3fb596gj5glz7jnhi0j',
        api_key_id='1853638c-1949-4db3-812f-c37b9b22c877'
    )
    return await RobotClient.at_address('irtest-main.unc6fit79p.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get webcam (camera component)
    thermal_camera = Camera.from_robot(robot, "thermal-cam")

    # Clear buffer 
    for _ in range(0,3):
        await thermal_camera.get_image()

    dir = "/home/ubuntu/data/thermal_camera/"

    # Start loop
    i = 0
    while True:
        try:
            image = await thermal_camera.get_image()
            now = datetime.now()

            filename = dir + "{}.jpg".format(now.isoformat('T'))
            image.save(filename)

            print("saving image: {}".format(filename))

            i = i + 1

        except Exception as e:
            print("Exception: " + str(e))

            if e == KeyboardInterrupt:
                break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())