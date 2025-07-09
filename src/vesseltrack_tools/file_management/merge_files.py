import sys
import os
import pandas as pd
import copy


def merge_files(_config):
    ais_directory_path = _config.get("ais_directory_path")
    if(ais_directory_path==None):
        print("Error: No AIS files directory path given.")
        return
    output_file_path = _config.get("output_file_path", ais_directory_path)

    print(f"\tMerging AIS files from {ais_directory_path}.")

    df = []
    for file in os.listdir(ais_directory_path):
        if(file[0]=='.'):
            continue
        df.append(copy.deepcopy(pd.read_csv(ais_directory_path+'/'+file)))
    df = pd.concat(df)
    df.to_csv(output_file_path+"/merged_positions.csv", index=False)
    print(f"\tCreated a merged file of AIS tracks at {output_file_path}/merged_positions.csv.")

    










if __name__ == "__main__":
  
    import json

    config_file = open(sys.argv[1], "r",encoding="utf-8")
    CONFIG = json.load(config_file)
    merge_files(CONFIG)
