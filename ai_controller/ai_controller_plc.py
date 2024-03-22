import asyncio
import time
import json

from viam.robot.client import RobotClient
from viam.components.generic import Generic
from speech_service_api import SpeechService
from viam.components.board import Board

pins = {
    "1": ["one", "1"],
    "2": ["two", "2"],
    "3": ["three", "3"],
    "4": ["four", "4", "for"]
}

# Create context
async def create_context(filepath):
        # Open files
        f = open(filepath)
        context_map = json.load(f)
        f.close()

        # Add header to context
        context = context_map["header"]

        # Add action to context
        actions = context_map["actions"]
        for key in actions:
            context = context + " Action {0} ".format(key)

            if len(actions[key]) > 1:
                context = context + "can be"
            else:
                context = context + "is"

            i = 0
            for i in range(len(actions[key])):
                value = actions[key][i]
                context = context + " {0}".format(value)

                if i == len(actions[key])-1:
                    context = context + "."
                    break

                context = context + " or"

        return context

# Check input for possible pin number representations
def extract_pin(pin, pin_representations, request):
    for pin_rep in pin_representations:
        if pin_rep in request:
            return pin
        
    return ""

# Extract any pin number from input
def extract_digital_pin_from_input(request):
    for key in pins.keys():
        p = extract_pin(key, pins[key], request)
        if p != "":
            return p
    return ""

# Set the state of all digital pins
async def set_digital_pin_state(gpiopin, response):
    if "1" in response:
        print('turning on {0}'.format(response))
        await gpiopin.set(True)
    elif "2" in response:
        print('turning off {0}'.format(response))
        await gpiopin.set(False)
    elif "3" in response:
        print('restarting {0}'.format(response))
        await gpiopin.set(False)
        time.sleep(1)
        await gpiopin.set(True)
    return

# Get the status of all defined pins
async def get_pin_states(plcboard):
    pin_states = ""

    i = 0
    for pin in pins.keys():
        output = await plcboard.gpio_pin_by_name("DO_0{0}".format(pin))
        s = await output.get()
        pin_states = pin_states + "pin {0} is {1}".format(pin, s)
        if i != len(pins)-1:
            pin_states = pin_states + ", "
        else :
            pin_states = pin_states + "."
        i = i + 1

    return pin_states


class AIController():

    def __init__(self):
        return

    @classmethod
    async def send_chatgpt(self, message):
        resp = {}
        try:
            req = {"request": message}
            resp = await self.chatgptprocessor.do_command(req)
            print("RESPONSE: " + resp["response"]+ "\n")    
            
        except Exception as e:
            print("error processing request, please try again: ")
            print(e)
            return ""

        return resp["response"]

    @classmethod
    async def handle_action_input(self, input):
        context = await create_context("contexts/chatgpt_plc_actions.json")
        print(" - context: ", context)

        message=[
            {"role": "system", "content": context},
            {"role": "user", "content": input}
        ]            

        response = await self.send_chatgpt(message)

        # If a gpio pin action is detected, actuate accordingly 
        if 'action' in response: 
            pin = extract_digital_pin_from_input(input)
            if pin == "": 
                return

            gpiopin = await self.plcboard.gpio_pin_by_name("DO_0{0}".format(pin))

            await set_digital_pin_state(gpiopin,response)

    @classmethod
    async def handle_status_check(self, input):
        # Check for status request
        if "status" not in input:
            return

        # Get state of pins
        pin_states = await get_pin_states(self.plcboard)
        print(" - pin_states: ", pin_states)

        # Get context 
        context = await create_context("contexts/chatgpt_plc_status_check.json")
        print(" - context: ", context)

        message=[
            {"role": "system", "content": context},
            {"role": "user", "content": pin_states}
        ]

        # -------------------------------------------------------------------------
        resp = await self.send_chatgpt(message)
        if resp == "":
            return
        # -------------------------------------------------------------------------

        # Output speech
        await self.audioout.do_command({"message": resp})

        return
    
    @classmethod
    async def handle_input(self, input):
        # Handle status request
        if "status" in input or "state" in input:
            await self.handle_status_check(input)

        await self.handle_action_input(input)

    @classmethod
    async def init(self, robot):

        self.speech = SpeechService.from_robot(robot, name="speech-to-text") 
        print("Text to speech service initialized")

        self.chatgptprocessor = Generic.from_robot(robot, "chat-gpt-processor") 
        print("Get chat-gpt-connection (generic component)  initialized")  

        self.audioout = Generic.from_robot(robot, "sound_player") 
        print("Sound player initialized")

        self.plcboard = Board.from_robot(robot, "PLCBoard")
        print("Chat-gpt-connection (generic component) initialized")

        # Start loop
        i = 0
        while True:
            if i > 10000:
                break
            
            inputs = await self.speech.get_commands(1)
            print("INPUTS: ", inputs)
            if len(inputs) > 0:
                await self.handle_input(inputs[0])

            i = i + 1
            time.sleep(1)

async def connect():
    opts = RobotClient.Options.with_api_key(
      api_key='n7fyemvc4qfo9ho1okzbjr4w6s30jceq',
      api_key_id='6023a294-cd6c-4ad9-813d-a88db0574e5a'
    )
    return await RobotClient.at_address('laptop-chat-gpt-main.muhvcb3otx.viam.cloud', opts)

async def main():
    robot = await connect()

    ai_controller = AIController()
    await ai_controller.init(robot)

    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())