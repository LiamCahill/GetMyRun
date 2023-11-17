import datetime


class RunEventDTO:
    day = datetime.MINYEAR
    date = datetime.MINYEAR
    run = 0

    def __init__(self, day=None, date=None, run=None):
        if day is None:
            print("Default constructor called for day")
            day = datetime.MINYEAR
        if date is None:
            print("Default constructor called for date")
            day = datetime.MINYEAR
        if run is None:
            print("Default constructor called for run")
            run = "Default run"

        self.day = day
        self.date = date
        self.RunPlan = run

    def getDay(self):
        return self.day

    def getDate(self):
        return self.date

    def getRun(self):
        return self.run

    def weekday_helper(raw_date):
        #6/8/2023
        date_info = raw_date.split("/")
        day = date_info[0]
        month = date_info[1]
        year = date_info[2]
        print(f'sliced info here: day: {month}, month: {day}, year: {year}')
        weekday = datetime.date(int(year), int(month), int(day)).weekday()
        print(f'weekday: {weekday}')

        #print(f'weekday_helper {raw_date} and weekday is: {weekday}')

