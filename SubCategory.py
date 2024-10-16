class SubCategory:
    
    def __init__(self, idSubCategory, Name, idCategory):
        self.idSubCategory = idSubCategory
        self.Name = Name
        self.idCategory = idCategory
        
    @staticmethod
    def from_dict(source):
        product = SubCategory(source['idSubCategory'], source['Name'], source['idCategory'])
        return product

    def to_dict(self):
        dest = {"idSubCategory": self.idSubCategory, 'Name': self.Name, 'idCategory': self.idCategory}
        return dest
        

    def __repr__(self):
        return f"SubCategory(\
                idSubCategory= {self.idSubCategory},\
        Name= {self.Name},\
        idCategory= {self.idCategory}\
            )"