from app import db
class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    ticker_symbol=db.Column(db.String(255), unique=True, nullable=False,primary_key=True)
    avg_buy_price=db.Column(db.Float)
    shares=db.Column(db.Integer)

    def __init__(self, ticker_symbol, avg_buy_price, shares):
        """initialize with name."""
        self.ticker_symbol=ticker_symbol
        self.avg_buy_price=avg_buy_price
        self.shares=shares

    def add_trade(self):
        db.session.add(self)
        db.session.commit()
    
    def fetch_all():
        return Portfolio.query.all()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return "<Portfolio: {}>".format(self.ticker_symbol)
    

class Trades(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    ticker_symbol=db.Column(db.String(255), nullable=False)
    price=db.Column(db.Float)
    shares=db.Column(db.Integer)
    type=db.Column(db.String(10))


    def __init__(self, id,ticker_symbol, price, shares, type):
        """initialize with name."""
        if id!=-1:
            self.id = id
        self.ticker_symbol = ticker_symbol
        self.price = price
        self.shares = shares
        self.type = type


    def add_trade(self):
        db.session.add(self)
        db.session.commit()
    
    def fetch_all():
        return Trades.query.all()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return "<Trades: {}>".format(self.ticker_symbol)
    
