import asyncio
import argparse
import os
import pytz

from datetime import datetime, timedelta
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions, Credentials
from viam.proto.app.data import Filter

async def main(delete_data):
    data_directory = '/Users/jeremyhyde/Development/uad-dataset/realsense_camera'

    og_dir = data_directory + "/pcd/"
    new_dir = data_directory + "/pcd_temp/"

    for filename in os.listdir(data_directory + "/pcd/"):
        index = filename[:-4].rfind(".")
        new_filename = filename[:index] + "-" + filename[index+1:]
        print(new_filename)
        os.rename(og_dir + filename, new_dir + new_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-delete_past_data')
    args = parser.parse_args()
    delete_data  = False
    if args.delete_past_data == "true":
        delete_data = True
    asyncio.run(main(delete_data))