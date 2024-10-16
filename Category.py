class Category:
    
    def __init__(self, idCategory, Name, code):
        self.Name = Name
        self.code = code
        self.idCategory = idCategory
        
    @staticmethod
    def from_dict(source):
        product = Category(source['idCategory'], source['Name'], source['code'])
        return product

    def to_dict(self):
        dest = {"idCategory": self.idCategory, 'Name': self.Name, 'code': self.code}
        return dest

    def __repr__(self):
        return f"Category(\
                idCategory= {self.idCategory},\
        Name= {self.Name},\
        code= {self.code}\
            )"