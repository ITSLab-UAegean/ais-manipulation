from haversine import haversine, Unit

def distance(lon1, lat1, lon2, lat2, unit='km'):
    return haversine((lat1, lon1), (lat2, lon2), unit=unit) 

def distance_rev(lat1, lon1, lat2, lon2, unit='km'):
    return haversine((lat1, lon1), (lat2, lon2), unit=unit) 


def mae_lists(l1, l2, rev=False, unit='km'):
    # Provides the mean absolute error (MAE) from two lists of the same length, in the given metric (default is km),
    # when rev==False, the coordinates are given as (lon, lat) and conversely for True.
    if((len(l1)==0) or (len(l1)!=len(l2))):
        return 0
    count = 0
    for i in range(len(l1)):
        if(rev==True):
            count += distance_rev(l1[i][0], l1[i][1], l2[i][0], l2[i][1], unit)
        else:
            count += distance(l1[i][0], l1[i][1], l2[i][0], l2[i][1], unit)
    return count / len(l1)

def mae_dataframes(df1, df2, col_lon='LON', col_lat='LAT', unit='km'):
    # Provides the mean absolute error (MAE) from two dataframes of the same length, in the given metric (default is km),
    # The columns that have 
    if((len(df1)==0) or (len(df1)!=len(df2))):
        return 0
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=('_left', '_right'))
    count = 0
    for _, row in df.iterrows():
        count += distance(row[f'{col_lon}_left'], row[f'{col_lat}_left'], row[f'{col_lon}_right'], row[f'{col_lat}_right'], unit)
    return count / len(df)








if __name__ == "__main__":
    coords = input('Please give the first location coordinates (lon, lat) separated by comma: ').split(',')
    lon1 = float(coords[0])
    lat1 = float(coords[1])
    coords = input('Please give the second location coordinates (lon, lat) separated by comma: ').split(',')
    lon2 = float(coords[0])
    lat2 = float(coords[1])

    res = distance(lon1, lat1, lon2, lat2, 'nmi')
    print(f'The distance between the given points is : {res} (nautical miles)')