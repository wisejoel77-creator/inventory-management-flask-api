from flask import Flask,requests
app = Flask(__name__)

inventory = []

@app.route('/viewitem', methods=['GET'])
def view_inventory_item():
    return inventory

@app.route("/inventory/<int:item_id>")
def get_item(item_id):
    if 0 <= item_id < len(inventory):
        return inventory[item_id]
    else:
        return "Item not found", 404

@app.route('/removeitem', methods=['DELETE'])
def remove_inventory_item():
    return 'Item removed from inventory! no content', 204

@app.route('/edititem', methods=['PATCH'])  
def update_inventory_item():
    return 'Item updated in inventory!'

@app.route('/additem', methods=['POST'])
def add_inventory_item():
    return 'Item added to inventory!',201

if __name__ == '__main__':
    app.run(port=5555, debug=True)