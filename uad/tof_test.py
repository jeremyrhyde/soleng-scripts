import asyncio
from datetime import datetime
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor 


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='lk1ww7musa7fupenpophj9s2rupr013a',
        api_key_id='d6ebf20e-7ed1-4ac0-b8e7-0365358902de'
    )
    return await RobotClient.at_address('toftest-main.unc6fit79p.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get tof (sensor component)
    tof_sensor = Sensor.from_robot(robot, "tof-sensor")

    dir = "/home/ubuntu/data/tof_sensor/"

    # Start loop
    while True:
        i = 0
        now = datetime.now()
        with open(dir + "tof_results_{}.csv".format(now.isoformat('T')), 'w', newline='') as file:
            writer = file.writer(file)
            try:
                while i < 1000:
                    # Get readings
                    readings = await tof_sensor.get_readings()
                    now = datetime.now()

                    if i == 0:
                        keys = readings.keys
                        keys.insert(0, "Time")
                        writer.writerow(keys)

                    values = readings.values
                    values.insert(0, now.isoformat('T'))

            except Exception as e:
                print("Exception: " + str(e)) 
                
                if e == KeyboardInterrupt:
                    break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())