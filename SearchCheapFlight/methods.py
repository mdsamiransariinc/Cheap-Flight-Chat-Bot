
class bookflight:

    def __init__ (self):
        self.Depcode = ""
        self.Departure  =""
        self.destination =""
        self.DesCode = ""
        self.year = ""
        self.month = ""
        self.day = ""
        self.adult = ""
        self.children = "0"
        self.infants = "0"
        self.Depdate = ""
        self.Retdate = ""

    def setDestination(self, DesCode, destination):
        self.DesCode = DesCode
        self.destination = destination

    def setDeparture(self,DepCode, departure):
        self.DepCode = DepCode
        self.Departure = departure


    def getFormatDate(self,year, month, day):
        if( len(year) == 2):
            year = "20" + year
        if( len(month) == 1):
            month = "0" + month
        if( len(day) == 1):
            day = "0" + day
        return f"{year}-{month}-{day}"

    def setDepdate(self,year, month, day):
        self.Depdate = self.getFormatDate(year, month, day)
        

    def setRetdate(self,year, month, day):
        self.Retdate = self.getFormatDate(year, month, day)

    def setSeats(self,adult,children,infants):
        self.adult = adult
        self.children = children
        self.infants = infants