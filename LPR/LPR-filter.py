import asyncio
from PIL import Image
from typing import List
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient, Detection
import os
from viam.media.utils.pil import pil_to_viam_image, CameraMimeType


async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='nsunpbrmbo1o9jlkz2cmzxliwpxvonrw',
        api_key_id='0aba5aae-5d3e-4905-a64c-d57564160b81'
    )
    return await RobotClient.at_address('laptop-marriott-main.muhvcb3otx.viam.cloud', opts)

def get_best_detection(detections: List[Detection], label: str, threshold: float):
    max_confidence = threshold
    best_detection = None
    for detection in detections:
        if detection.confidence > max_confidence and (detection.x_max-detection.x_min)*(detection.y_max-detection.y_min) != 0 and detection.class_name == label:
            best_detection = detection
    return best_detection

async def main():
    robot = await connect()

    # Recognize car & license plates
    car_detector = VisionClient.from_robot(robot, "car-detector")

    # Start loop
    i = 0
    skip_count = 0
    count = 0
    threshold = 0.8 

    dir = "/Users/jeremyhyde/Development/marriott-ev-data"
    results_dir = "/Users/jeremyhyde/Development/marriot_filter_results"
    files = os.listdir(dir)

    new_dir = results_dir + "/threshold_{}".format(threshold)
    os.mkdir(new_dir)

    for file in files:
        i = i + 1
        print("{}/{} -- IMAGES FOUND: {}".format(i,len(files), count), end='\r')

        try:
            image = Image.open(dir + "/" + file)
            vimage = pil_to_viam_image(image.convert('RGB'), CameraMimeType.JPEG)

            detections = await car_detector.get_detections(vimage)     
            detection = get_best_detection(detections, "Car", threshold)

            # Check for detections
            if detection == None:
                continue

            image.save(new_dir + "/" + file)
            count = count + 1
        except Exception as e:
            skip_count = skip_count + 1
            print("skipping")

    print()
    print("Total images passing filter ({}) = {}/{}".format(threshold, count, len(files)))
    print("Total images skipped due to error = {}/{}".format(skip_count, len(files)))


    # Don't forget to close the machine when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())