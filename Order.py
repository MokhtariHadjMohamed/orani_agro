class Order:
    
    def __init__(self, deliveryBoyId, idClient, idOrder, orderSituation, productOrders):
        self.deliveryBoyId = deliveryBoyId
        self.idClient = idClient
        self.idOrder = idOrder
        self.orderSituation = orderSituation
        self.productOrders = productOrders
        
    @staticmethod
    def from_dict(source):
        order = Order(source['deliveryBoyId'], source['idClient'], source['idOrder'],
                    source['orderSituation'], source['productOrders'])
        return order

    def to_dict(self):
        dest = {"deliveryBoyId": self.deliveryBoyId, 'idClient': self.idClient, 'idOrder': self.idOrder,
                'orderSituation': self.orderSituation, 'productOrders': self.productOrders}
    
        return dest
        

    def __repr__(self):
        return f"Order(\
                deliveryBoyId={self.deliveryBoyId},\
        idClient= {self.idClient},\
        idOrder= {self.idOrder},\
        orderSituation= {self.orderSituation},\
        productOrders= {self.productOrders}\
            )"