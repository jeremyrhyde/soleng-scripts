# play_sound

This collection of python scripts can be used to play sound bytes when a face is detected. FOR DEMO PURPOSE ONLY.

## Usage

These scripts are to be used with the play-sounds module located in the [Registry](https://app.viam.com/module/jeremyrhyde/play-sound).

## Deploy to robot

1. Extract sound and deepfaces folders zip files
2. Setup robot using [example config](https://github.com/jeremyrhyde/soleng-scripts/blob/main/play_sound/example_config.json), editing the `pictures_directory` to point to your extracted copy of 'deepfaces' download and the `video path` to use your desired camera via the discovery service.
3. Edit api_key, api_key_id and address in face_detection_with_sound.py to those associated with your robot
4. (Optional) Edit the face-to-sound.json to point at your extracted copy of 'sounds' and update the referenced '.json' on line 26 of `face_detection_with_sound.py`.