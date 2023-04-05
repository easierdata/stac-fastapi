import json
import os
import pathlib
import subprocess
import fnmatch
import urllib.parse

def compute_cid(file_path):
    cid = subprocess.check_output(["ipfs", "add", "-q", file_path]).decode().strip()
    return cid

def process_landsat_scene(landsat_directory):
    input_stac_filename = None

    for file in os.listdir(landsat_directory):
        if fnmatch.fnmatch(file, '*_stac.json'):
            input_stac_filename = file
            break

    if not input_stac_filename:
        print("No stac.json file found in the specified directory.")
        return

    input_stac_path = os.path.join(landsat_directory, input_stac_filename)
    output_stac_filename = input_stac_filename.replace("_stac.json", "_stac_web3_enriched.json")
    output_stac_path = os.path.join(landsat_directory, output_stac_filename)

    with open(input_stac_path) as input_file:
        stac_data = json.load(input_file)

    for asset_name, asset_data in stac_data["assets"].items():
        href = asset_data["href"]
        file_name = os.path.basename(urllib.parse.urlparse(href).path)
        file_path = os.path.join(landsat_directory, file_name)
        
        if pathlib.Path(file_path).is_file():
            cid = compute_cid(file_path)
            if "IPFS" not in asset_data["alternate"]:
                asset_data["alternate"]["IPFS"] = {}
            asset_data["alternate"]["IPFS"]["href"] = f"ipfs://{cid}"
        else:
            print(f"File not found for asset: {asset_name}")

    with open(output_stac_path, "w") as output_file:
        json.dump(stac_data, output_file, indent=4)

if __name__ == "__main__":
    # Set current directory to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    landsat_directory = "LC09_L1TP_015033_20221015_20221015_02_T1"

    process_landsat_scene(landsat_directory)
