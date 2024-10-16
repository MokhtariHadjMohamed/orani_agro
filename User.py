class User:
    
    def __init__(self, idUser, name, familyName, address,
                 phone, email, invitation, typeUser, latitude, longitude):
        self.idUser = idUser
        self.name = name
        self.familyName = familyName
        self.address = address
        self.phone = phone
        self.email = email
        self.invitation = invitation
        self.type = typeUser
        self.latitude = latitude
        self.longitude = longitude
        
        
    @staticmethod
    def from_dict(source):
        user = User(source['idUser'], source['name'], source['familyName'],
                    source['address'], source['phone'], source['email'], 
                    source['invitation'], source['type'], source['latitude'], source['longitude'])
        return user

    def to_dict(self):
        dest = {"idUser": self.idUser, 'name': self.name, 'familyName': self.familyName,
                "address": self.address, 'phone': self.phone, 'email': self.email,
                'invitation': self.invitation, 'type': self.type, 'latitude': self.latitude, 
                'longitude': self.longitude}
    
        return dest
        

    def __repr__(self):
        return f"User(\
                idUser={self.idUser},\
        name= {self.name},\
        familyName= {self.familyName},\
        address= {self.address},\
        phone= {self.phone},\
        email= {self.email},\
        invitation= {self.invitation},\
        latitude= {self.latitude},\
        longitude= {self.longitude},\
        type= {self.type}\
            )"