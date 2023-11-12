import datetime


class RunEventDTO:
    day = datetime.MINYEAR
    date = datetime.MINYEAR
    run = 0

    def __init__(self, day, date, run):
        self.day = day
        self.date = date
        self.RunPlan = run

    def getDay(self):
        return self.day

    def getDate(self):
        return self.date

    def getRun(self):
        return self.run
