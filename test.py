import datetime

date = datetime.datetime.now()
for i in range(16):
    date += datetime.timedelta(days=1)
    print(date.date().strftime('%Y/%m/%d'))