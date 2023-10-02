# definē produkta klasi un konstruktoru
class GardenProduct:
    def __init__(self, name, quantity, product_type, variety):
        self.name = name
        self.quantity = quantity
        self.product_type = product_type
        self.variety = variety

    def make_jam(self, jam_quantity):
        if self.product_type == "Auglis" and self.quantity >= jam_quantity * 2:  # izveido ievārījumu tikai no augļiem
            self.quantity -= jam_quantity * 2
            return GardenProduct(f"Ievārījums - {self.name}", jam_quantity, "Ievārījums", "")

