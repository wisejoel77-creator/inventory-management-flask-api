#app.py file for the inventory management system
from flask import Flask,request,jsonify
import requests
from inventory import inventory
app = Flask(__name__)

#route to get all inventory items
@app.route('/inventory', methods=['GET'])
def view_all_inventory_items():
    return jsonify(inventory),200

#route to get a specific inventory item by its ID
@app.route("/inventory/<int:item_id>")
def get_specific_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"message": "Item not found"}), 404

#route to remove an inventory item by its ID
@app.route('/removeitem/<int:item_id>', methods=['DELETE'])
def remove_inventory_item(item_id):
    global inventory

    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item removed from inventory!"}), 204

#route to update an existing inventory item
@app.route('/edititem/<int:item_id>', methods=['PATCH'])  
def update_inventory_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    # Update the item with new data
    for key in data:
        if key in item:  
            item[key] = data[key]

    return jsonify({"message": "Item updated in inventory!"}),201

#route to add a new inventory item
@app.route('/additem', methods=['POST'])
def add_inventory_item():
    data = request.get_json()

    new_item = {"id": len(inventory) + 1, "name": data.get("name"), "barcode": data.get("barcode"), "quantity": data.get("quantity"), "price": data.get("price") }
    inventory.append(new_item)
    return jsonify({"message": "Item added to inventory!"}), 201

#external API route to get product details by barcode
@app.route('/product/<barcode>', methods=['GET'])
def get_product_details(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        product_data = response.json()
        if product_data.get("status") == 1:
            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Product not found"}), 404
    else:
        return jsonify({"message": "Error fetching product details"}), response.status_code

if __name__ == '__main__':
    app.run(port=5555, debug=True)