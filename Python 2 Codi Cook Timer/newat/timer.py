import datetime

StartDate = "10/10/11"

date_1 = datetime.datetime.strptime(StartDate, "%m/%d/%y")

end_date = date_1 + datetime.timedelta(seconds=10)

print end_date
