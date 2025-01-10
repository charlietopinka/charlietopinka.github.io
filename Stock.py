class Stock:
    def __init__(self, name=None, abbr=None, shares=0, price=0.0, percent_change = 0.0):
        self.name = name
        self.abbr = abbr
        self.shares = shares
        self.price = price
        self.total = 0.0
        self.percent_change = percent_change
