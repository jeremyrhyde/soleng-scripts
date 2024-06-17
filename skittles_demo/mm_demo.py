import asyncio
import time

from viam.robot.client import RobotClient
from viam.components.camera import Camera 
from viam.components.motor import Motor 
from viam.services.vision import VisionClient

rev = 10
rpm = 60

confidence_level = 0.5

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='9gnzzaaap6641bmhjts06cf9qxhawe1r',
        api_key_id='a73abb37-59e1-4b24-9c6e-82e887eb8538'
    )
    return await RobotClient.at_address('m-m-demo-main.dxg9k7h3iq.viam.cloud', opts)

async def handle_refill_classification(classifications, motor):

    refill = "No"
    for classification in classifications:
        if classification.class_name == "refill":
            if classification.confidence > confidence_level:
                refill = "yes"
                await motor.go_for(rpm, rev) 
            print("Refill required: {} ({}%)".format(refill, str(round(classification.confidence*100))))

async def handle_red_classification(classifications):
    print("--------------------\nDetections")

    max_class = ""
    max_confidence = 0
    for classification in classifications:
        if classification.confidence > max_confidence:
            max_confidence = classification.confidence
            max_class = classification.class_name
    print("Anomaly detection: {} ({}%)".format(max_class, str(round(classification.confidence*100))))

async def main():
    robot = await connect()

    # Get webcam (camera component)
    webcam = Camera.from_robot(robot, "webcam")

    # Get refill_detector (vision service)
    refill_detector = VisionClient.from_robot(robot, "refill_detector")

    # Get red_detector (vision service)
    red_detector = VisionClient.from_robot(robot, "red_detector")

    # Get sound_player (generic component)
    motor = Motor.from_robot(robot, "stepper")

    # Start loop
    input("Press <Enter> to start: ")
    while True:
        try:
            # Get image after clearing buffer
            for _ in range(0,3):
                await webcam.get_image()
            webcam_return_value = await webcam.get_image()

            # Handle red detections
            red_classifications = await red_detector.get_classifications(webcam_return_value, 1)
        
            if len(red_classifications) == 0:
                print("No classifications made..., weird right?")

            await handle_red_classification(red_classifications)

            # Handle refill detections
            refill_classifications = await refill_detector.get_classifications(webcam_return_value, 1)
        
            if len(refill_classifications) == 0:
                print("No classifications made..., weird right?")

            await handle_refill_classification(refill_classifications, motor)

            time.sleep(10)
        except Exception as e:
            print("Error: ", str(e))
            break

    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())