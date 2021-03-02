from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#Configs
from configs.configurations import Development, Testing, Production

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)


#Models
from models.inventory import Inventory
from models.stock import Stock
from models.sales import Sales

#Services
from services.inventory import InventoryService

#@app.before_first_request
#def create():
    #db.create_all()
    


@app.route('/')
def index():
    return render_template("/landing/index.html")

@app.route('/admin')
def admin():
    return InventoryService.inventories()


if __name__ =="__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
