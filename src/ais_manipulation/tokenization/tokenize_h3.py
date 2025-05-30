import h3
import sys
import pandas as pd



def create_token_series(df, col = 'h3_cell_9'):
    for col in df.columns:
        if('h3_cell' in col):
            break

    prev = ''
    prev_t = 0
    cells = []
    starts = []
    ends = []
    pos_counts = []

    for _, row in df.iterrows():
        if(row[col]!=prev):
            cells.append(row[col])
            starts.append(row['TIMESTAMP'])
            if(prev!=''):
                ends.append(prev_t)
                pos_counts.append(counter)
            counter = 1
            prev = row[col]
        else:
            counter += 1
        prev_t = row['TIMESTAMP']
    else:
        ends.append(prev_t)
        pos_counts.append(counter)

    res = pd.DataFrame({col:cells, 'TIMESTAMP_ENTER':starts, 'TIMESTAMP_LEAVE':ends, 'NO_POSITIONS': pos_counts})
    res['MMSI'] = df.iloc[0]['MMSI']
    return res



def alex():
    print('yolt')





if __name__ == "__main__":
  import json

  config_file = open(sys.argv[1], "r",encoding="utf-8")
  CONFIG = json.load(config_file)
#   tokenize_file_h3(CONFIG)