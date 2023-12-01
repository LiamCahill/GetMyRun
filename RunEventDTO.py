import datetime


class RunEventDTO:
    # day = datetime.MINYEAR
    # date = datetime.MINYEAR
    # run = ""

    def __init__(self, day, date, run):
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
        date_info = raw_date.split("/")
        month = date_info[0]
        day = date_info[1]
        year = date_info[2]
        weekday = datetime.date(int(year), int(month), int(day)).weekday()

    #def getWeekday(weekday_int):


