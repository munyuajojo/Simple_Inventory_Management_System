from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine

#e = create_engine("postgresql://postgres:jojo@localhost/inventories", pool_recycle=3600)
#c = e.connect()

#Configs
from configs.configurations import Development, Testing, Production

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:jojo@localhost/inventories"


#Models
from models.inventory import Inventory
from models.stock import Stock
from models.sales import Sales

#Services
from services.inventory import InventoryService

#Error Handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template("/errors/404.html"), 404

@app.before_first_request
def create():
   db.create_all()
    


@app.route('/')
def index():
    return render_template("/landing/index.html")

@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    if request.method == 'POST':
        InventoryService.add_inventory()
        
    return InventoryService.inventories()
    render_template("/admin/inventories.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("/admin/dashboard.html")



@app.route('/stock', methods=['GET', 'POST'])
def stock():
    return render_template("/admin/stock.html")


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    return render_template("/admin/sales.html")


@app.route('/users', methods=['GET', 'POST'])
def users():
    return render_template("/admin/users.html")

#@app.errorhandler(404)
#def page_not_found(error):
    #return render_template("/errors/404.html"), 404

if __name__ =="__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


