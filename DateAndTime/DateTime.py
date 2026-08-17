from datetime import datetime, time, timedelta, date
from zoneinfo import ZoneInfo

# timezone = ZoneInfo('Asia/Kolkata')
# now = datetime.now(tz=timezone)



# TODAY = datetime.now()
# print(TODAY.time())
# print(date.today())

# dateB = datetime.strptime('03-08-2026','%d-%m-%Y')
# print(dateB)

# dateB = dateB.replace(tzinfo=timezone)
# print(datetime.combine(now, time=time(8,59,50)))

datetime1 = '25/12/2026'
datetime2 = datetime.strptime(datetime1,'%d/%m/%Y')
print(datetime2.strftime('%d-%m-%Y'))


# print(now-dateB)
# print(datetime.strftime(now + timedelta(days=1),'%d-%m-%Y'))