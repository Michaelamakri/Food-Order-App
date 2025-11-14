class order:
    def __init__(self, order_id, status:str, total_price:float=0.0):
        self.order_id=order_id
        self.status=status
        self.total_price=total_price
    def AddItem(self, item_name: str, price: float):
        self.items.append((item_name, price))
        self.total_price += price

    def finalize(self):
        self.status = "Completed"
    


    

        