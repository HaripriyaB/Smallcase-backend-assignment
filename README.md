## Smallcase Backend Assignment-Portfolio tracking API
The aim of this task is to create an API which tracks the trades happening for every security.

## Tech stack
* Python 3
* Flask
* Postgresql
* Virtualenv

## Endpoints
The base url for this application is \
**https://smallcase-app-1.herokuapp.com/**

The routes are as follows:
### `https://smallcase-app-1.herokuapp.com/trade` 
Purpose: Adding trades for a security(either BUY/SELL)[POST], Updating the trade fields[PUT] and fetching all trades[GET]. This route accepts 3 verbs GET, PUT, POST.
* The GET method takes optional param `ticker` whose value is the ticker symbol.
* The POST method takes body in the following format:
Example:
[id is optional here]
```
    "id" : <Optional>,
    "price": 10,
    "shares": 6,
    "ticker_symbol": "WIPRO",
    "type": "SELL"
```
* The PUT method takes body int the following format:
Example: [id is compulsory here]
```
    "id": 1,
    "price": 10.0,
    "shares": 10,
    "ticker_symbol": "TCS",
    "type": "BUY"
```
### `https://smallcase-app-1.herokuapp.com/portfolio` 
Purpose : Fetch portfolio which is an aggregate view of all securities in the portfolio with its final quantity and average buy price[GET].
* The GET method lists all the securities and average buy price along with shares count
### `https://smallcase-app-1.herokuapp.com/trade/<int:id>/delete`
Purpose: A trade of a security can be removed from the portfolio reverting the changes it had when it was added[DELETE].
* The DELETE method deletes that trade which has id as given id and reflects the changes in portfolio as well.

### `https://smallcase-app-1.herokuapp.com/returns`
Purpose: The cumulative returns is calculated as `SUM((CURRENT_PRICE[ticker] - AVERAGE_BUY_PRICE[ticker]) * CURRENT_QUANTITY[ticker])` and this sum is returned as response.
* The GET method fetches the cumulative return value of the current portfolio.
