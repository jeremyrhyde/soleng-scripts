import asyncio
import argparse
import os
import pytz

from datetime import datetime, timedelta
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions, Credentials
from viam.proto.app.data import Filter, BinaryID

async def main(delete_data):
    dataset_id = "66e9e2e5285c1e65825f039c"

    # Prod
    dial_opts = DialOptions.with_api_key('umuygfvg6p6ukzde00hdbaucknxeao74','12c9d6aa-a40b-498f-a785-d2904d11132d')

    app_client = await ViamClient.create_from_dial_options(dial_opts, "app.viam.com")
    data_client = app_client.data_client

    filter = Filter(
        component_name = "ev-cam-0.6",
        location_ids=["b2fkxt2kv3"],
        organization_ids=["63dc6cce-cee8-427f-844b-7a7c55390241"]
    )
    (binary_data,_,_) = await data_client.binary_data_by_filter(
        filter= filter,
        limit = 1000,
        include_binary_data = False
    )
    print(binary_data)
    my_binary_ids = []
    for data in binary_data:
        my_binary_ids.append(BinaryID(file_id = data.metadata.id, organization_id="63dc6cce-cee8-427f-844b-7a7c55390241", location_id="b2fkxt2kv3"))

    print("Number of ids: " + str(len(my_binary_ids)))
    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=my_binary_ids,
        dataset_id=dataset_id
    )
    
    print("Result: Successfully uploaded data\n")


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