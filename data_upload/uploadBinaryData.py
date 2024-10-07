import asyncio
import argparse
import os
import pytz

from datetime import datetime, timedelta
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions, Credentials
from viam.proto.app.data import Filter

async def main(delete_data):
    data_directory = '/Users/jeremyhyde/Development/marriot_filter_results/threshold_0.6'

    component_type="rdk:component:camera"
    method_name="GetImage"
    component_name = "ev-cam-0.6"

    # Prod
    part_id = "fa9508b9-e9ab-4825-8a20-f3ce23262afa"
    dial_opts = DialOptions.with_api_key('umuygfvg6p6ukzde00hdbaucknxeao74','12c9d6aa-a40b-498f-a785-d2904d11132d')

    app_client = await ViamClient.create_from_dial_options(dial_opts, "app.viam.com")
    data_client = app_client.data_client

    # # Delete existing data.
    # if delete_data:
    #     await data_client.delete_binary_data_by_filter(Filter(part_id=part_id))
    #     print("Deleted old data associated with part_id: " + part_id)

    files = os.listdir(data_directory)
    index = 0
    for filename in files:
        file_path = os.path.join(data_directory, filename)
        print("Uploading Binary File {}/{}".format(index+1, len(files)))
        if os.path.isfile(file_path):
            print("Filename: " + filename)

        i = filename.rfind(".")
        datetime_str = filename[:i]
        
        est = pytz.timezone('US/Eastern')
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.utc)
        #datetime_obj = datetime_obj.astimezone(tz = est) + timedelta(hours = 1)
        print("Time: " + str(datetime_obj)+ " (" + str(datetime_obj.tzinfo) + ")\n")
        
        file = open(file_path, mode='rb')
        data = file.read()
        file.close()

        try:
            # async def binary_data_capture_upload(
            #     self,
            #     binary_data: bytes,
            #     part_id: str,
            #     component_type: str,
            #     component_name: str,
            #     method_name: str,
            #     file_extension: str,
            #     method_parameters: Optional[Mapping[str, Any]] = None,
            #     tags: Optional[List[str]] = None,
            #     data_request_times: Optional[Tuple[datetime, datetime]] = None,
            # ) -> str:
            await data_client.binary_data_capture_upload(
                part_id=part_id,
                component_type=component_type,
                component_name=component_name,
                method_name=method_name,
                binary_data=data,
                file_extension=".jpg",
                data_request_times=(datetime_obj, datetime_obj) ,
            )
            print("Result: Successfully uploaded data\n")
        except Exception as e: 
            print("Result: Failed to upload " + method_name + " data due to upload exception")
            print(e)

        index = index +1 

    print("Upload complete")
    app_client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-delete_past_data')
    args = parser.parse_args()
    delete_data  = False
    if args.delete_past_data == "true":
        delete_data = True
    asyncio.run(main(delete_data))