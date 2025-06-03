"""_summary_

Functions related to projecting vessel type name.

"""
from math import isnan

def get_vessel_type_dataframe(pos):
    n = -1
    for i in pos.TYPE.unique():
        if(not isnan(i)):
            n = i
            break
    return get_vessel_type(n)

def get_vessel_type(n):
    """_summary_

    Possible vessel types:
        # All
        # Cargo
        # Dredging or Underwater ops
        # High Speed Craft
        # Fishing
        # Military and Law Enforcement
        # Passenger
        # Pleasure Craft
        # Sailing
        # Service
        # Tanker
        # Tug and Towing
        # Other
        # Unknown

    Args:
        pos (_type_): input

    Returns:
        _type_: _description_
    """


    if(n>69 and n<80):
        return 'Cargo'
    if(n>79 and n<90):
        return 'Tanker'
    if(n==33):
        return 'Dredging'
    if(n>39 and n<50):
        return 'HSC'
    if(n==30):
        return 'Fishing'
    if(n==35 or n==55):
        return 'Military_Law'
    if(n>59 and n<70):
        return 'Passenger'
    if(n==37):
        return 'Pleasure'
    if(n==36):
        return 'Sailing'
    if(n in [50, 51, 53, 54, 58]):
        return 'Service'
    
    if(n in [31, 32, 52]):
        return 'Tug'
    if(n==-1):
        return 'Unknown'
    return 'Other'
