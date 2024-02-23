# LPR

This collection of Python scripts can be used to extract license plates from images and return the associated text. FOR DEMO PURPOSE ONLY.

## Usage

These scripts are to be used with the YOLOv5 module located in the [Registry](https://app.viam.com/module/viam-labs/YOLOv5) and an [OCR](https://github.com/felixreichenbach/tesseract-ocr) implementation made by Felix.

The YOLOv5 model used comes from [Hugging Faces](https://huggingface.co/keremberke/yolov5m-license-plate).

## Deploy to robot

1. Download and install [OCR](https://github.com/felixreichenbach/tesseract-ocr) using the associated instructions
2. Download the YOLOv5 model [Hugging Faces](https://huggingface.co/keremberke/yolov5m-license-plate)
3. Set up your robot using [example config](https://github.com/jeremyrhyde/soleng-scripts/blob/main/LPR/example_config.json), edit the local module to link to your copy of the OCR build and edit the  `model_location` to point your copy of the YOLOv5 model.
4. Edit api_key, api_key_id and address in face_detection_with_sound.py to those associated with your robot.