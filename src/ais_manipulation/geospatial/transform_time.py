from datetime import datetime, timezone


def time_string_to_epoch(date, form = "%Y-%m-%d %H:%M:%S"):  
    try:
        res = datetime.strptime(date, form).replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        res = -1
    return int(res)




if __name__ == "__main__":
    option = input('Please select the input format to be transformed: date or timestamp. \n')
    if(option=='date'):
        date = input('Please give the date in the following format (%Y-%m-%d %H:%M:%S). \n')
        print(time_string_to_epoch(date))
    elif(option=="timestamp"):
        print(0)