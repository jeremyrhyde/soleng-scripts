import asyncio
import argparse
import os
from PIL import Image

from datetime import datetime, timedelta
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions, Credentials
from viam.proto.app.data import Filter

class DD():
    
    app_client : None
    api_key_id: str
    api_key: str
    dataset_name: str = ""
    dataset_id: str = ""
    tags: list = []
    labels: list = []
    binary_ids: dict
    image_index: dict

    async def new(self) -> None:
        self.api_key = "76tnaq1s9gv33eg2s7w9fohhoav9km2l"
        self.api_key_id = "fa209be2-f1fc-4aca-8b1a-fbedf252e389"

    async def viam_connect(self) -> ViamClient:
        dial_options = DialOptions.with_api_key( 
            api_key=self.api_key,
            api_key_id=self.api_key_id
        )
        return await ViamClient.create_from_dial_options(dial_options)

    async def get_binary_ids(self, dataset_id, tags, labels):
            filter_id = self.filter_id(dataset_id, tags, labels)

            if not filter_id in self.binary_ids:
                # lookup ids from data management
                self.binary_ids[filter_id] = []

                filter_args = {}
                if dataset_id != "":
                    filter_args['dataset_id'] = dataset_id
                if len(tags) > 0:
                    filter_args['tags_filter'] =  TagsFilter(tags=tags)
                filter = Filter(**filter_args)
                if len(labels) > 0:
                    filter_args['bbox_labels'] = labels
                filter = Filter(**filter_args)

                binary_args = {'filter': filter, 'include_binary_data': False}
                # we need to page through results
                done = False
                while not done:
                    binary_ids = await self.app_client.data_client.binary_data_by_filter(**binary_args)
                    if len(binary_ids[0]):
                        self.binary_ids[filter_id].extend(binary_ids[0])
                        binary_args['last'] = binary_ids[2]
                    else:
                        done = True
            return self.binary_ids[filter_id]

    async def get_next_binary_image(self, dataset_id, tags, labels, binary_ids) -> Image:
            filter_id = self.filter_id(dataset_id, tags, labels)
            if not filter_id in self.image_index:
                self.image_index[filter_id] = 0
            
            binary_id = BinaryID(
                file_id = binary_ids[self.image_index[filter_id]].metadata.id,
                organization_id = binary_ids[self.image_index[filter_id]].metadata.capture_metadata.organization_id,
                location_id = binary_ids[self.image_index[filter_id]].metadata.capture_metadata.location_id
            )

            self.image_index[filter_id] = self.image_index[filter_id] + 1
            if (self.image_index[filter_id] >= len(binary_ids)):
                self.image_index[filter_id] = 0
            
            binary_data = await self.app_client.data_client.binary_data_by_ids(binary_ids=[binary_id])
            return Image.open(BytesIO(binary_data[0].binary))


async def main():
    delete_data = False
    outdir = '/Users/jeremyhyde/Downloads/test_data'
    #data_directory = input_dir + '/data'

    organizational_id = "53e2a500-3fa0-4ad6-9844-098769838d87"
    location_id="dxg9k7h3iq"
    machine_id="7426ef85-4d09-441e-a99a-c46977c99e7a"
    machine_part_id = "66fac649-88f5-44da-a61d-35d86f4e2c03"

    d = DD()
    d.new()

    viam_client = await d.viam_connect()
    # # Prod
    # dial_opts = DialOptions(
    #     auth_entity='artemis-main.muhvcb3otx.viam.cloud',
    #     credentials=Credentials(
    #         type='robot-location-secret',
    #         payload="nsza58lfef9f53f3m0esnxghwlxkcwhj0kqdedxhcxsxa86z"
    #     )
    # )

    # # # Dev
    # # part_id = "f402dcab-ef8e-4047-9e6e-0260bd5b819d"
    # # dial_opts = DialOptions(
    # #     auth_entity='slam-qa-robot--do-not-use--main.nd46y9thju.viamstg.cloud',
    # #     credentials=Credentials(
    # #         type='robot-location-secret',
    # #         payload="4j2ipfkoznc43wktk4ofsx5dwadvfi50gjuanlep5ivaw5uj"
    # #     )
    # # )

    # app_client = await ViamClient.create_from_dial_options(dial_opts, "app.viam.com")
    # data_client = app_client.data_client

    # # Delete existing data.
    # if delete_data:
    #     await data_client.delete_binary_data_by_filter(Filter(part_id=part_id))
    #     print("Deleted old data associated with part_id: " + part_id)

    # numFiles = len(os.listdir(data_directory))
    # index = 0
    # for filename in os.listdir(data_directory):
    #     # if index > 10:
    #     #     break
    #     file_path = os.path.join(data_directory, filename)
    #     print("Uploading Binary File " + str(index) + "/" + str(numFiles))
    #     if os.path.isfile(file_path):
    #         print("Filename: " + filename)

    #     datetime_str = filename[:filename.find("Z")+1]
        
    #     est = pytz.timezone('US/Eastern')
    #     datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.utc)
    #     datetime_obj = datetime_obj.astimezone(tz = est) + timedelta(hours = 1)
    #     print("Time: " + str(datetime_obj)+ " (" + str(datetime_obj.tzinfo) + ")\n")
        
    #     file = open(file_path,mode='rb')
    #     data = file.read()
    #     file.close()

    #     try:
    #         await data_client.binary_data_capture_upload(
    #             part_id=part_id,
    #             component_type=component_type,
    #             component_name=component_name,
    #             method_name=method_name,
    #             binary_data=data,
    #             file_extension=".pcd",
    #             data_request_times=(datetime_obj, datetime_obj) ,
    #         )
    #         print("Result: Successfully uploaded PCD data\n")
    #     except Exception as e: 
    #         print("Result: Failed to upload " + method_name + " data due to upload exception")
    #         print(e)

    #     index = index +1 

    # print("Upload complete")
    # app_client.close()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('-delete_past_data')
    # args = parser.parse_args()
    # delete_data  = False
    # if args.delete_past_data == "true":
    #     delete_data = True
    asyncio.run(main())