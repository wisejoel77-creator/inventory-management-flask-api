#app.py file for the inventory management system
from urllib import response

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

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        # Debug step (VERY useful while learning)
        print("STATUS CODE:", response.status_code)

        if response.status_code != 200:
            return jsonify({"error": "External API error"}), 502
        data = response.json()

        if data.get("status") != 1:
            return jsonify({"error": "Product not found"}), 404
        product = data.get("product", {})

        return jsonify({
            "barcode": barcode,
            "name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text")
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504

    except requests.exceptions.RequestException as e:
        print("REQUEST FAILED:", e)
        return jsonify({"error": "Failed to fetch product details"}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)