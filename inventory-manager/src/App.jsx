/*app.jsx file for the inventory management system */
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [newItem, setNewItem] = useState({name: "",barcode: "",quantity: "",price: "",});
  const [inventory, setInventory] = useState([]);
  const [barcode, setBarcode] = useState("");

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

  return (
    <div className="container">

      <h1>Inventory Management System</h1>
      <h2>Add Item</h2>
      <form onSubmit={addItem}>
  <input name="name" placeholder="Name" value={newItem.name} onChange={handleChange}/>
  <input name="barcode" placeholder="Barcode" value={newItem.barcode} onChange={handleChange}/>
  <input name="quantity" placeholder="Quantity" value={newItem.quantity} onChange={handleChange}/>
  <input name="price"  placeholder="Price"  value={newItem.price}  onChange={handleChange} />
  <button type="submit">Add Item</button>
</form>

      <h2>search product</h2>
      <div classname = "Search-box">
        <input type="text"placeholder="Search by barcode..."value={barcode}onChange={(e) => setBarcode(e.target.value)}/>
      </div>

      {inventory.filter((item) => (item.barcode.toString().includes(barcode))).map((item) => (
        <div className="card" key={item.id}>
          <h3>{item.name}</h3>
          <p>Barcode: {item.barcode}</p>
          <p>Quantity: {item.quantity}</p>
          <p>Price: ${item.price}</p>
          <button onClick={() => deleteItem(item.id)}>Delete</button>
        </div>
      ))}

    </div>
  );
}


export default App;