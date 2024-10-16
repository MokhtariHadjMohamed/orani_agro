class ProductOrder:
    
    def __init__(self, idClient, idOrder, idProduct, quantity,
                 orderSituation, productName, productPrice):
        self.idClient = idClient
        self.idOrder = idOrder
        self.orderSituation = orderSituation
        self.idProduct = idProduct
        self.quantity = quantity
        self.productName = productName
        self.productPrice = productPrice
        
    @staticmethod
    def from_dict(source):
        order = ProductOrder(source['idClient'], source['idOrder'], source['idProduct'],
                            source['quantity'], source['orderSituation'],
                            source['productName'], source['productPrice'])
        return order

    def to_dict(self):
        dest = {"idClient": self.idClient, 'idOrder': self.idOrder, 'orderSituation': self.orderSituation,
                'idProduct': self.idProduct, 'quantity': self.quantity, 'productName': self.productName,
                'productPrice': self.productPrice}
    
        return dest
        

    def __repr__(self):
        return f"ProductOrder(\
                idClient={self.idClient},\
        idOrder= {self.idOrder},\
        orderSituation= {self.orderSituation},\
        idProduct= {self.idProduct},\
        quantity= {self.quantity},\
        productName= {self.productName},\
        productPrice= {self.productPrice}\
            )"