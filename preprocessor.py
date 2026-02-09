import pandas as pd
import re

def preprocess(data):

    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm))\s-\s(?:(.*?):\s)?(.*)'

    df_data = []

   
    for line in data.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            datetime = match.group(1)
            sender = match.group(2) if match.group(2) else "System"
            message = match.group(3)

            df_data.append([sender, message , datetime])

    
    df = pd.DataFrame(df_data, columns=["User" ,  "Message", "Date-Time"])

    df["Date-Time"] = pd.to_datetime(
                    df["Date-Time"],
                    dayfirst=True,      # because format is DD/MM/YY
                    errors="coerce"     # if something fails, it becomes NaT instead of error
                    )
    
    df['Year'] = df['Date-Time'].dt.year
    df['month_num'] = df['Date-Time'].dt.month
    df['only_date'] = df['Date-Time'].dt.date
    df['day_name'] = df['Date-Time'].dt.day_name()
    df['Month'] = df['Date-Time'].dt.month_name()
    df['Date'] = df['Date-Time'].dt.day
    df['Hour'] = df['Date-Time'].dt.hour
    df['Minute'] = df['Date-Time'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df