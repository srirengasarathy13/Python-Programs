from datetime import datetime, time, timedelta, date
from zoneinfo import ZoneInfo





Today = datetime.now()
# print(Today.time())
# print(date.today())

# dateB = datetime.strptime('03-08-2026','%d-%m-%Y')
# print(dateB)

Today = Today.replace(2003,5,6)
# print(Today)

# datetime1 = '25/12/2026'
# datetime2 = datetime.strptime(datetime1,'%d/%m/%Y')

# print(today-datetime2)

# print(datetime.strftime(today + timedelta(days=1),'%d-%m-%Y'))

timezone = ZoneInfo('Asia/Tokyo')
now = datetime.now(tz=timezone)
print(now)