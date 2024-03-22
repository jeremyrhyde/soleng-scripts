import asyncio
import time
import json

from PIL import Image 
from datetime import datetime, timedelta

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera 
from viam.components.generic import Generic
from viam.services.vision import VisionClient
from speech_service_api import SpeechService
from viam.components.board import Board
from viam.components.motor import Motor
from viam.components.base import Base
from viam.components.encoder import Encoder


async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='n7fyemvc4qfo9ho1okzbjr4w6s30jceq',
      api_key_id='6023a294-cd6c-4ad9-813d-a88db0574e5a'
    )
    return await RobotClient.at_address('laptop-chat-gpt-main.muhvcb3otx.viam.cloud', opts)

async def connectrover():
    opts = RobotClient.Options.with_api_key(
      api_key='zrp0hhptaxrgg15hn5fx99rzjjmxfe0d',
      api_key_id='57d521ca-cad7-4486-9d20-f3dba1b11733'
    )
    return await RobotClient.at_address('hades-main.muhvcb3otx.viam.cloud', opts)


async def main():
    robot = await connect()
    rover = await connectrover()

    speech = SpeechService.from_robot(robot, name="speech-to-text")

    # Get chat-gpt-connection (generic component)
    chatgptprocessor = Generic.from_robot(robot, "chat-gpt-processor")


    # Get chat-gpt-connection (generic component)
    roverbase = Base.from_robot(rover, "viam_base")

    # Start loop
    i = 0
    while True:
        if i > 1000:
            break
        
        commands = await speech.get_commands(1)
        print("commands ", commands)

        if len(commands) > 0:
            print("-------------------------------------------------------------")
            req = {"request": commands[0]}
            print("REQUEST : " + req["request"])
            resp = {}
            try:
                resp = await chatgptprocessor.do_command(req)
                
            except Exception as e:
                print("error processing request, please try again")
                continue

            print("RESPONSE : " + resp["response"])

            print("-------------------------------------------------------------")

            if 'action' in resp["response"]: 
                if "1" in resp["response"]:
                    print('move forwards')
                    await roverbase.move_straight(400,200)
                elif "2" in resp["response"]:
                    print('move backwards')
                    await roverbase.move_straight(-400,200)
                elif "3" in resp["response"]:
                    print('spin to the left')
                    await roverbase.spin(200,200)
                elif "4" in resp["response"]:
                    print('spin to the right')
                    await roverbase.spin(-200,200)
                else:
                    continue
            
        i = i + 1

        time.sleep(1)


    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())