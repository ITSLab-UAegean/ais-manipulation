import h3
import sys
import pandas as pd


def transform_point_h3(lon, lat, h3_resolution):
   return h3.latlng_to_cell(lat, lon, h3_resolution)


def tokenize_file_h3(_config):

  ais_file_path = _config.get("ais_file_path")
  output_file_path =  _config.get("output_file_path")
  if((ais_file_path == None) or  (output_file_path==None)):
    print("Error: no input / output file path given.")
    return
  col_lon = _config.get("lon_column", "LON")
  col_lat = _config.get("lat_column", "LAT")
  h3_resolutions = _config.get("h3_resolution", [9])

  df = pd.read_csv(ais_file_path)
  for res in h3_resolutions:
    df[f'h3_cell_{res}'] = df.apply(lambda row: h3.latlng_to_cell(row[col_lat], row[col_lon], res), axis=1)

  df.to_csv(output_file_path, index=False)






if __name__ == "__main__":
  import json

  config_file = open(sys.argv[1], "r",encoding="utf-8")
  CONFIG = json.load(config_file)
  tokenize_file_h3(CONFIG)