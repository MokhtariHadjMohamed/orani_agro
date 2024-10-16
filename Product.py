class Product:
    
    def __init__(self, IDCategorie, NameProduct, PrixCarton, PrixUnitaire, Quantite, idProduct):
        self.IDCategorie = IDCategorie
        self.NameProduct = NameProduct
        self.PrixCarton = PrixCarton
        self.PrixUnitaire = PrixUnitaire
        self.Quantite = Quantite
        self.idProduct = idProduct
        
    @staticmethod
    def from_dict(source):
        product = Product(source['IDCategorie'], source['NameProduct'], source['PrixCarton'],
                    source['PrixUnitaire'], source['Quantite'], source['idProduct'])
        return product

    def to_dict(self):
        dest = {"IDCategorie": self.IDCategorie, 'NameProduct': self.NameProduct, 'PrixCarton': self.PrixCarton,
                'PrixUnitaire': self.PrixUnitaire, 'Quantite': self.Quantite, 'idProduct': self.idProduct}
        return dest
        

    def __repr__(self):
        return f"Product(\
                IDCategorie{self.IDCategorie},\
        NameProduct= {self.NameProduct},\
        PrixCarton= {self.PrixCarton},\
        PrixUnitaire= {self.PrixUnitaire},\
        Quantite= {self.Quantite},\
        idProduct= {self.idProduct}\
            )"