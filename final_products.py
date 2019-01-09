class Products(object):

    def __init__(self, rowid, name, price):
        self.rowid = rowid
        self.name = name
        self.price = price

    def product_info(self):
        return self.rowid, self.name, self.price
