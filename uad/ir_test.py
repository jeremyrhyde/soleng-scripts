import asyncio
import csv
from datetime import datetime
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor 


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key="<API_KEY>",
        api_key_id="<API_KEY_ID>"
    )
    return await RobotClient.at_address('toftest-main.unc6fit79p.viam.cloud', opts)

async def main():
    robot = await connect()

    # Get tof (sensor component)
    tof_sensor = Sensor.from_robot(robot, "tof-sensor")

    dir = "/home/ubuntu/data/tof_sensor/"

    # Start loop
    i = 0
    now = datetime.now()
    with open(dir + "tof_results_{}.csv".format(now.isoformat('T')), 'w', newline='') as file:
        writer = csv.writer(file)
        while i < 1000:
            print("{}/1000".format(i))
            try:
                # Get readings
                readings = await tof_sensor.get_readings()
                now = datetime.now()

                if i == 0:
                    keys = list(readings.keys())
                    keys.insert(0, "Time")
                    writer.writerow(keys)

                values = list(readings.values())
                values.insert(0, now.isoformat('T'))
                writer.writerow(values)

                i = i + 1
            except Exception as e:
                print("Exception: " + str(e)) 
                
                if e == KeyboardInterrupt:
                    break
            

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())