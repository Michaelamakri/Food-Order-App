class Restaurant:
    def __init___(self, name:str, rest_id, phone, email:str,menu):
        self.name=name
        self.rest_id=rest_id
        self.phone=phone
        self.email=email
        self.menu={}
    def AddMenuItem(self, item_name: str, price: float):
        self.menu[item_name] = price



