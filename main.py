from flask import Flask, render_template, request, flash, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine

#e = create_engine("postgresql://postgres:jojo@localhost/inventories", pool_recycle=3600)
#c = e.connect()

#Configs
from configs.configurations import Development, Testing, Production

app = Flask(__name__)
#app.config.from_object(Development)
app.config.from_object(Testing)
db = SQLAlchemy(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:jojo@localhost/inventories"


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


@app.context_processor
def utility_processor():
    def compute_quantity(inventoryID: int):
        #Find an inventory that matches the ID
        inv= Inventory.get_inventory_byID(id=inventoryID)
        if inv is not None:
            #Get the Stock Quantity
            total_stock = list(map(lambda obj:obj.quantity, inv.stock))
            total_sales = list(map(lambda obj:obj.quantity, inv.sales))

            return sum(total_stock) - sum(total_sales)

    return dict(compute_quantity=compute_quantity)


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
    total_inventories = len(Inventory.fetch_all())
    return render_template("/admin/dashboard.html", total_inventories=total_inventories)



@app.route('/stock')
def stock():
    all_stock=Stock.fetch_all()
    return render_template("/admin/stock.html", all_stock=all_stock)


@app.route('/sales')
def sales():
    all_sales=Sales.fetch_all()
    return render_template("/admin/sales.html", all_sales=all_sales)


@app.route('/users', methods=['GET', 'POST'])
def users():
    return render_template("/admin/users.html")


@app.route("/inventories/<int:inv_id>/restock", methods=['POST'])
def restock(inv_id):
    if request.method == 'POST':
        qty = request.form['qty']
        r = Stock(quantity=qty, inventoryId=inv_id)
        r.create_record()
        flash('New stock successfully added!', 'success')

    return redirect(url_for('inventories'))


@app.route("/inventories/<int:inv_id>/makesale", methods=['POST'])
def makesale(inv_id):
    if request.method == 'POST':
        qty = request.form['qty']
        s = Sales(quantity=qty, inventoryId=inv_id)
        s.create_record()
        flash('A new sale was successfully made!', 'success')

    return redirect(url_for('inventories'))


@app.route("/inventories/<int:inv_id>/edit", methods=['POST'])
def edit_inventory(inv_id):
    if request.method == 'POST':
        name = request.form['name']
        itype = request.form['category']
        bp = request.form['bp']
        sp = request.form['sp']

        u = Inventory.edit_inventory(
            inv_id=inv_id,
            name=name,
            itype=itype,
            bp=bp,
            sp=sp
        )
        flash('Inventory record successfully updated!', 'success')

    return redirect(url_for('inventories'))

if __name__ =="__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


