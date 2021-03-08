from flask import render_template, request, redirect, url_for

#Models
from models.inventory import Inventory
from models.stock import Stock
from models.sales import Sales

class InventoryService:

    @classmethod
    def inventories(cls):
        #Get all Inventories
        all_inventories = Inventory.fetch_all()
        print("Here:", all_inventories)
        return render_template("/admin/inventories.html", inventories=all_inventories)

    @classmethod
    def add_inventory(cls):
        if request.method == 'POST':
            name = request.form['name']
            itype = request.form['category']
            bp = request.form['bp']
            sp = request.form['sp']


            #Check if the Inventory name exist
            if Inventory.check_inventory_exists(inventory_name=name):
                print("The inventory already exists")
                return redirect(url_for('inventories'))
            else:
                record = Inventory(
                    name=name.title(),
                    itype=itype.title(),
                    bp=bp,
                    sp=sp
                )
                record.create_record()
                print("success!")
                return redirect(url_for('inventories'))

            
        