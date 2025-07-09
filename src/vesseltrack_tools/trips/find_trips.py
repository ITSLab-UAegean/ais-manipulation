import pandas as pd
import sys

MIN_MMSI_POSITIONS = 10
MIN_STOP_POSITIONS = 4
MIN_TRIP_POSITIONS = 10
MAX_TRIP_GAP = 60*60*1 # 1 hour
IDLE_SPEED_THRESHOLD = 1 # knot


def refine_trips_selection(df):
    temp = df.groupby('TRIP').count()
    new_trips = list(temp[temp['TIMESTAMP']>=MIN_TRIP_POSITIONS].index)
    df['TRIP'] = df.apply(lambda row: row['TRIP'] if(row['TRIP'] in new_trips) else 'idle', axis=1)
    
    return df


def assign_trip(ts, trips_times, trips_names):
    for i in range(len(trips_times)):
        trip = trips_times[i]
        if((ts>=trip[0]) and (ts<trip[1])):
            return trips_names[i]
    else:
        return 'idle'


def find_trips(df):
    df.drop_duplicates(subset=['TIMESTAMP'], keep='first', inplace=True)
    if(len(df)<MIN_MMSI_POSITIONS):
        return

    idle = True
    # idle_counter = 0
    # cur_start = 0
    trips_times = []
    trips_names = []
    prev_t = df.iloc[0]['TIMESTAMP']
    
    for _, row in df.iterrows():
        cur_t = row['TIMESTAMP']
        if(idle == False):
            dt = cur_t - prev_t
            if(dt > MAX_TRIP_GAP):
                # close previous trip
                trips_times.append((cur_start, cur_t))
                trips_names.append(f'{df.name}_{cur_start}_{prev_t}')
                
                if(row['SPEED'] >= IDLE_SPEED_THRESHOLD): 
                    # initialize new trip
                    idle_counter = 0
                    cur_start = cur_t
                else:
                    idle = True

            elif(row['SPEED'] < IDLE_SPEED_THRESHOLD):
                idle_counter += 1
                if(idle_counter == 1):
                    # set trip end point
                    cur_stop = prev_t
                elif(idle_counter >= MIN_STOP_POSITIONS):
                    idle = True
                    # close previous trip
                    trips_times.append((cur_start, cur_stop))
                    trips_names.append(f'{df.name}_{cur_start}_{cur_stop}')
        
        else:
            if(row['SPEED'] >= IDLE_SPEED_THRESHOLD):
                idle = False
                # initialize new trip
                idle_counter = 0
                cur_start = cur_t
        
        prev_t = cur_t

    else:
        if(idle == False):
            # close previous trip
            trips_times.append((cur_start, prev_t+1))
            trips_names.append(f'{df.name}_{cur_start}_{cur_t}')

    df['TRIP'] = df.apply(lambda row: assign_trip(row['TIMESTAMP'], trips_times, trips_names), axis=1)
    df = refine_trips_selection(df)
         
    return df


def find_trips_file(_config):
    ais_file_path = _config.get('ais_file_path')
    if(ais_file_path==None):
        print("Error: No AIS file path given.")
        return
    output_file_path = _config.get("output_file_path", ais_file_path.split('.csv')[0]+'_trips.csv')

    print(f"\tAssigning trips for AIS file from {ais_file_path} to {output_file_path}.")

    df = pd.read_csv(ais_file_path)
    trips = df.groupby('MMSI').apply(find_trips, include_groups=False).reset_index()
    trips.drop('level_1', axis=1, inplace=True)
    trips.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    import json
    config_file = open(sys.argv[1], "r",encoding="utf-8")
    CONFIG = json.load(config_file)
    find_trips_file(CONFIG)
