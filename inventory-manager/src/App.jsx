/*app.jsx file for the inventory management system */
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [newItem, setNewItem] = useState({name: "",barcode: "",quantity: "",price: "",});
  const [inventory, setInventory] = useState([]);
  const [barcode, setBarcode] = useState("");
  const [editingItemId, setEditingItemId] = useState(null);
  const [editItem, setEditItem] = useState({ name: "", barcode: "", quantity: "", price: "" });
  const [apiProduct, setApiProduct] = useState(null);
  const [searchBarcode, setSearchBarcode] = useState("");

  function addItem(e) {
    e.preventDefault();
    fetch("http://127.0.0.1:5555/additem", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newItem),
    })
      .then((response) => response.json())
      .then(() => {
        return fetch("http://127.0.0.1:5555/inventory");
  })
      .then((response) => response.json())
      .then((data) => {
        setInventory(data);
      });

        setNewItem({ name: "", barcode: "", quantity: "", price: "" });
  }

  function handleChange(e) {
  setNewItem({
    ...newItem,
    [e.target.name]: e.target.value,
  });
}

function fetchProduct() {
  fetch(`http://127.0.0.1:5555/product/${searchBarcode}`)
    .then((res) => res.json())
    .then((data) => {
      setApiProduct(data);
    })
    .catch((err) => console.error("Product fetch failed:", err));
}

useEffect(() => {
  fetchInventory();
}, []);

function fetchInventory() {
  fetch("http://127.0.0.1:5555/inventory")
    .then((res) => res.json())
    .then((data) => setInventory(data))
    .catch((error) => console.error("Error fetching inventory:", error));
}
function deleteItem(id) {
  fetch(`http://127.0.0.1:5555/removeitem/${id}`, {
    method: "DELETE",
  }).then(() => fetchInventory());
}

function updateItem(id) {
  fetch(`http://127.0.0.1:5555/edititem/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(editItem),
  })
    .then((res) => res.json())
    .then(() => {fetchInventory();
      setEditingItemId(null);
    })
    .catch((err) => console.error("Update failed:", err));
}

 return (
  <div className="container">
    <h1>Inventory Management System</h1>

    <h2>Add Item</h2>
    <form onSubmit={addItem}>
      <input name="name" value={newItem.name} onChange={handleChange} placeholder="Name" />
      <input name="barcode" value={newItem.barcode} onChange={handleChange} placeholder="Barcode" />
      <input name="quantity" value={newItem.quantity} onChange={handleChange} placeholder="Quantity" />
      <input name="price" value={newItem.price} onChange={handleChange} placeholder="Price" />
      <button type="submit">Add Item</button>
    </form>

    <h2>Search</h2>
    <input value={barcode} onChange={(e) => setBarcode(e.target.value)} placeholder="Search barcode"/>

    <h2>External Product Lookup</h2>

<input
  placeholder="Enter barcode" value={searchBarcode}
  onChange={(e) => setSearchBarcode(e.target.value)}/>

<button onClick={fetchProduct}>Search Product</button>

{apiProduct && (
  <div className="card">
    <h3>{apiProduct.name}</h3>
    <p><strong>Brand:</strong> {apiProduct.brand}</p>
    <p><strong>Barcode:</strong> {apiProduct.barcode}</p>
  </div>
)}

    {inventory.filter((item) => item.barcode.toString().includes(barcode))
      .map((item) => (
        <div className="card" key={item.id}>
          <h3>{item.name}</h3>
          <p>Barcode: {item.barcode}</p>
          <p>Quantity: {item.quantity}</p>
          <p>Price: ${item.price}</p>
    <button onClick={() => deleteItem(item.id)}>Delete</button>

          <button
            onClick={() => {setEditingItemId(item.id);
              setEditItem({ name: item.name, barcode: item.barcode, quantity: item.quantity, price: item.price,
              });
            }}> Edit
           </button>

          {editingItemId === item.id && (
            <div className="edit-form">
              <input name="name" value={editItem.name}
                onChange={(e) => setEditItem({ ...editItem, name: e.target.value })
                }/>

              <input name="barcode" value={editItem.barcode}
                onChange={(e) => setEditItem({ ...editItem, barcode: e.target.value })
                } />

              <input name="quantity" value={editItem.quantity}
                onChange={(e) => setEditItem({ ...editItem, quantity: e.target.value })
                }/>

              <input name="price" value={editItem.price}
                onChange={(e) =>  setEditItem({ ...editItem, price: e.target.value })
                } />

              <button onClick={() => updateItem(item.id)}>
                Save Changes
              </button>
            </div>
          )}
        </div>
      ))}
  </div>
); 
}

export default App;