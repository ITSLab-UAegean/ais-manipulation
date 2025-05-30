import pandas as pd



MIN_MMSI_POSITIONS = 10
MIN_STOP_POSITIONS = 4
MIN_TRIP_POSITIONS = 10
MAX_TRIP_GAP = 60*60*12 # half a day
IDLE_SPEED_THRESHOLD = 1 # knot


def refine_trips_selection(df):
    temp = df.groupby('TRIP').count()
    new_trips = list(temp[temp['TIMESTAMP']>=MIN_TRIP_POSITIONS].index)
    df['TRIP'] = df.apply(lambda row: row['TRIP'] if(row['TRIP'] in new_trips) else 'idle', axis=1)
    
    return df


def assign_trip(index, trips_indexes, trips_names):
    for i in range(len(trips_indexes)):
        trip = trips_indexes[i]
        if((index>=trip[0]) and (index<trip[1])):
            return trips_names[i]
    else:
        return 'idle'


def find_trips(df):
    if(len(df)<MIN_MMSI_POSITIONS):
        return

    idle = True
    # idle_counter = 0
    # cur_start = 0
    trips_indexes = []
    trips_names = []
    prev_t = df.iloc[0]['TIMESTAMP']
    
    for index, row in df.iterrows():
        cur_t = row['TIMESTAMP']
        if(idle == False):
            dt = cur_t - prev_t
            if(dt > MAX_TRIP_GAP):
                # close previous trip
                trips_indexes.append((cur_start_index, index))
                trips_names.append(f'{df.name}_{cur_start}_{prev_t}')
                
                if(row['SOG'] >= IDLE_SPEED_THRESHOLD): 
                    # initialize new trip
                    idle_counter = 0
                    cur_start = cur_t
                    cur_start_index = index
                else:
                    idle = True

            elif(row['SOG'] < IDLE_SPEED_THRESHOLD):
                idle_counter += 1
                if(idle_counter == 1):
                    # set trip end point
                    cur_stop = prev_t
                    cur_stop_index = index
                elif(idle_counter >= MIN_STOP_POSITIONS):
                    idle = True
                    # close previous trip
                    trips_indexes.append((cur_start_index, cur_stop_index))
                    trips_names.append(f'{df.name}_{cur_start}_{cur_stop}')
        
        else:
            if(row['SOG'] >= IDLE_SPEED_THRESHOLD):
                idle = False
                # initialize new trip
                idle_counter = 0
                cur_start = cur_t
                cur_start_index = index
        
        prev_t = cur_t

    else:
        if(idle == False):
            # close previous trip
            trips_indexes.append((cur_start_index, index+1))
            trips_names.append(f'{df.name}_{cur_start}_{cur_t}')

    # print(len(trips_indexes), trips_indexes, trips_names)

    df['TRIP'] = df.apply(lambda row: assign_trip(row.name, trips_indexes, trips_names), axis=1)
    df = refine_trips_selection(df)
         
    return df

