import os
from app import create_app,db
config_name='production' # config_name = "development"
app = create_app(config_name)
db.create_all()

if __name__ == '__main__':
    app.run()
