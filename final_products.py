class Products(object):

    def __init__(self, rowid, name, price):
        """Constructor for Products objects"""
        self.rowid = rowid
        self.name = name
        self.price = price

    def product_info(self):
        """Returns products information: id, name, price"""
        return self.rowid, self.name, self.price
