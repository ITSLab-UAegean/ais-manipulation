import sys
import pandas as pd


def split_file(_config):
    ais_file_path = _config.get("ais_file_path")
    if(ais_file_path==None):
        print("Error: no input file given.")
        return
    output_path = _config.get("output_path", "/".join(ais_file_path.split("/")[:-2])+"/")
    id_column = _config.get("id_column", "MMSI")

    df = pd.read_csv(ais_file_path)
    
    count = 0
    print(f"\tSpliting AIS files at {ais_file_path}.")
    for id in df[id_column].unique():
        df[df[id_column]==id].to_csv(f"{output_path}{id}_positions.csv", index=False)
        count += 1
    print(f"\tCreated {count} different files of AIS tracks at {output_path}.")






if __name__ == "__main__":
  
    import json

    config_file = open(sys.argv[1], "r",encoding="utf-8")
    CONFIG = json.load(config_file)
    split_file(CONFIG)
