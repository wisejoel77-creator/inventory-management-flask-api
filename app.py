#app.py file for the inventory management system
from flask import Flask,request,jsonify
import requests
from inventory import inventory
app = Flask(__name__)

#route to get all inventory items
@app.route('/viewitem', methods=['GET'])
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

@app.route('/removeitem', methods=['DELETE'])
def remove_inventory_item():
    data = request.get_json()
    global inventory

    item = next((item for item in inventory if item["id"] == data.get("id")), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory = [i for i in inventory if i["id"] != data.get("id")]
    return '', 204
    

@app.route('/edititem', methods=['PATCH'])  
def update_inventory_item():
    return jsonify({"message": "Item updated in inventory!"})

@app.route('/additem', methods=['POST'])
def add_inventory_item():
    return jsonify({"message": "Item added to inventory!"}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)