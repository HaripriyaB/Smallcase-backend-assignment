from os import abort

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.models import Portfolio, Trades
    with app.app_context():
        db.create_all()

    @app.route('/test')
    def main():
        return "Hello World"

    @app.route('/trade', methods=['GET', 'PUT', 'POST'])
    def trading():
        if request.method == 'GET':
            if request.args.get('ticker') != None:
                tradelist = Trades.fetch_all()
                results = []

                for trade in tradelist:
                    if(trade.ticker_symbol == request.args.get('ticker')):
                        obj = {
                            'id': trade.id,
                            'ticker_symbol': trade.ticker_symbol,
                            'price': trade.price,
                            'shares': trade.shares,
                            'type': trade.type
                        }
                        results.append(obj)
                response = jsonify(results)
                response.status_code = 200
                return response
            else:
                tradelist = Trades.fetch_all()
                results = []

                for trade in tradelist:
                    obj = {
                        'id': trade.id,
                        'ticker_symbol': trade.ticker_symbol,
                        'price': trade.price,
                        'shares': trade.shares,
                        'type': trade.type
                    }
                    results.append(obj)
                response = jsonify(results)
                response.status_code = 200
                return response
        elif request.method == 'PUT':
            id = str(request.data.get('id', ''))
            if not id:
                response = jsonify({'ERROR': 'ID field is required'})
                response.status_code = 400
                return response
            tradelist = Trades.query.filter_by(id=id).first()
            flag=0
            if not tradelist:
                flag=1

            if request.data.get('type') == 'SELL':
                check_portfolio = Portfolio.query.filter_by(
                    ticker_symbol=request.data.get('ticker_symbol')).first()
                if not check_portfolio or (check_portfolio.shares < request.data.get('shares')):
                    response = jsonify(
                        {'ERROR': 'Cannot sell when low/no shares available'})
                    response.status_code = 400
                    return response
            if flag==1:
                tradelist=Trades(id,str(request.data.get('ticker_symbol')),request.data.get('price'), request.data.get('shares')
                ,str(request.data.get('type')))
            else :
                tradelist.id = id
                tradelist.ticker_symbol = str(request.data.get('ticker_symbol'))
                tradelist.price = request.data.get('price')
                tradelist.shares = request.data.get('shares')
                tradelist.type = str(request.data.get('type'))

            if Portfolio.query.filter_by(ticker_symbol=request.data.get('ticker_symbol', '')).first():
                if tradelist.type == 'BUY':
                    current_portfolio = Portfolio.query.filter_by(
                        ticker_symbol=request.data.get('ticker_symbol', '')).first()
                    total = current_portfolio.shares * current_portfolio.avg_buy_price
                    total = total + (tradelist.price * tradelist.shares)
                    total = total / (tradelist.shares +
                                     current_portfolio.shares)
                    current_portfolio.avg_buy_price = total
                    current_portfolio.shares = tradelist.shares + current_portfolio.shares
                else:
                    current_portfolio = Portfolio.query.filter_by(
                        ticker_symbol=request.data.get('ticker_symbol', '')).first()
                    current_portfolio.shares = tradelist.shares + current_portfolio.shares

                current_portfolio.add_trade()
            else:
                portfolio = Portfolio(
                    tradelist.ticker_symbol, tradelist.price, tradelist.shares)
                portfolio.add_trade()

            tradelist.add_trade()
            if flag==1:
                response = jsonify({
                    'NOTE' : 'The Id provided does not exist so creating a new record as below',
                    'id': tradelist.id,
                    'ticker_symbol': tradelist.ticker_symbol,
                    'price': tradelist.price,
                    'shares': tradelist.shares,
                    'type': tradelist.type
                })
            else :
                response = jsonify({
                    'id': tradelist.id,
                    'ticker_symbol': tradelist.ticker_symbol,
                    'price': tradelist.price,
                    'shares': tradelist.shares,
                    'type': tradelist.type
                })
            response.status_code = 202
            return response
        elif request.method == 'POST':
            if request.data.get('id'):
                if Trades.query.filter_by(id=request.data.get('id', '')).first() and Trades.query.filter_by(ticker_symbol=request.data.get('ticker_symbol')).first():
                    response = jsonify({'ERROR': 'Record already exists'})
                    response.status_code = 200
                    return response
            if request.data.get('type') == 'SELL':
                check_portfolio = Portfolio.query.filter_by(
                    ticker_symbol=request.data.get('ticker_symbol')).first()
                if not check_portfolio or (check_portfolio.shares < request.data.get('shares')):
                    response = jsonify(
                        {'ERROR': 'Cannot sell when low/no shares available'})
                    response.status_code = 400
                    return response
            if request.data.get('id'):
                tradelist = Trades(request.data.get('id'), str(request.data.get('ticker_symbol')), request.data.get(
                    'price'), request.data.get('shares'), str(request.data.get('type')))
            else:
                tradelist = Trades(-1,str(request.data.get('ticker_symbol')), request.data.get(
                    'price'), request.data.get('shares'), str(request.data.get('type')))

            if Portfolio.query.filter_by(ticker_symbol=request.data.get('ticker_symbol')).first():
                if tradelist.type == 'BUY':
                    current_portfolio = Portfolio.query.filter_by(
                        ticker_symbol=request.data.get('ticker_symbol', '')).first()
                    total = current_portfolio.shares * current_portfolio.avg_buy_price
                    total = total + (tradelist.price * tradelist.shares)
                    total = total / (tradelist.shares +
                                     current_portfolio.shares)
                    current_portfolio.avg_buy_price = total
                    current_portfolio.shares = tradelist.shares + current_portfolio.shares
                else:
                    current_portfolio = Portfolio.query.filter_by(
                        ticker_symbol=request.data.get('ticker_symbol', '')).first()
                    current_portfolio.shares = tradelist.shares + current_portfolio.shares
                current_portfolio.add_trade()
            else:
                portfolio = Portfolio(
                    tradelist.ticker_symbol, tradelist.price, tradelist.shares)
                portfolio.add_trade()
            tradelist.add_trade()
            response = jsonify({
                'id': tradelist.id,
                'ticker_symbol': tradelist.ticker_symbol,
                'price': tradelist.price,
                'shares': tradelist.shares,
                'type': tradelist.type
            })
            response.status_code = 201

            return response
        else:
            response = jsonify({'ERROR': 'Illegal Operation'})
            response.status_code = 400
            return response

    @app.route('/trade/<int:id>/delete', methods=['DELETE'])
    def delete_trade(id):
        if request.method == 'DELETE':
            del_trade = Trades.query.filter_by(id=id).first()
            if del_trade:
                curr_portfolio = Portfolio.query.filter_by(
                    ticker_symbol=del_trade.ticker_symbol).first()
                if del_trade.type == 'BUY':
                    del_share = del_trade.shares
                    del_price = del_trade.price
                    curr_avg_price = curr_portfolio.avg_buy_price
                    curr_shares = curr_portfolio.shares
                    new_avg_price = ((curr_avg_price*curr_shares) -
                                     (del_price*del_share))/(curr_shares-del_share)
                    curr_portfolio.avg_buy_price = new_avg_price
                    curr_portfolio.shares = curr_shares-del_share
                    curr_portfolio.add_trade()
                    del_trade.delete()
                    response = jsonify({
                        'ticker_symbol': curr_portfolio.ticker_symbol,
                        'avg_buy_price': curr_portfolio.avg_buy_price,
                        'shares': curr_portfolio.shares
                    })
                    response.status_code = 201
                    return response
                else:
                    curr_portfolio.shares = curr_portfolio.shares-del_trade.shares
                    curr_portfolio.add_trade()
                    del_trade.delete()
                    response = jsonify({
                        'ticker_symbol': curr_portfolio.ticker_symbol,
                        'avg_buy_price': curr_portfolio.avg_buy_price,
                        'shares': curr_portfolio.shares
                    })
                    response.status_code = 201
                    return response
            else:
                response = jsonify({'ERROR': 'No record found for this id'})
                response.status_code = 404
                return response
        else:
            response = jsonify({'ERROR': 'Illegal Operation'})
            response.status_code = 400
            return response

    @app.route('/portfolio', methods=['GET'])
    def return_portfolio():
        if request.method == 'GET':
            portfolio_list = Portfolio.fetch_all()
            results = []
            for portfolio in portfolio_list:
                obj = {
                    'ticker_symbol': portfolio.ticker_symbol,
                    'avg_buy_price': portfolio.avg_buy_price,
                    'shares': portfolio.shares
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/returns', methods=['GET'])
    def fetch_returns():
        if request.method == 'GET':
            portfolio_list = Portfolio.fetch_all()
            sum = 0
            for portfolio in portfolio_list:
                sum = sum + ((100-portfolio.avg_buy_price)*portfolio.shares)
            response = jsonify({'Cumulative Returns': sum})
            response.status_code = 200
            return response
    return app
