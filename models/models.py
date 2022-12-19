class Person:
    """ Person class"""

    def __init__(self, name, id, adhar_no, imgfile, address, mobile_no, ptype, threat):
        self.name = name
        self.id = id
        self.adhar_no = adhar_no
        self.imgfile=imgfile
        self.address= address
        self.mobile_no=mobile_no
        self.ptype= ptype
        self.threat=threat

    def __repr__(self):
        return Person('{}', '{}', {},'{}','{}','{}','{}').format(self.id, self.name, self.mobile_no,self.adhar_no, self.imgfile, self.address, self.ptype, self.threat)



