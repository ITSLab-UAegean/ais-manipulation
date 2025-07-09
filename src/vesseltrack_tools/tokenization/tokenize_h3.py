import sys
import pandas as pd


def keep_col_values(df, col_keep = []):
    if (col_keep == []):
        return {}
        
    res = df[col_keep].apply(lambda cols: cols.loc[cols.first_valid_index()] 
                             if cols.first_valid_index() is not None else 'None')
    return res.to_dict()


def create_token_seq_trip(df, col_keep = []):

    if('TRIP' not in df.columns):
        trip = df.name
    else:
        trip = df.iloc[0]['TRIP']


    for col in df.columns:
        if('h3_cell' in col):
            break
    else:
        col = 'h3_cell_7'

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

    res = {col+'_seq':cells, 'TIMESTAMP_ENTER':starts, 'TIMESTAMP_LEAVE':ends, 'NO_POSITIONS': pos_counts}
    res.update(keep_col_values(df, col_keep))
    res['TRIP'] = trip
    return res
 

if __name__ == "__main__":
  import json

  config_file = open(sys.argv[1], "r",encoding="utf-8")
  CONFIG = json.load(config_file)