/*app.jsx file for the inventory management system */
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [newItem, setNewItem] = useState({name: "",barcode: "",quantity: "",price: "",});
  const [inventory, setInventory] = useState([]);

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

  function searchItem() {

  }

  function handleChange(e) {
  setNewItem({
    ...newItem,
    [e.target.name]: e.target.value,
  });
}

  useEffect(() => {
    fetch("http://127.0.0.1:5555/inventory")
      .then((response) => response.json())
      .then((data) => {setInventory(data);
      })
      .catch((error) => {console.log(error); });
  }, []);

  return (
    <div className="container">

      <h1>Inventory Management System</h1>
      <h2>Add Item</h2>

      {inventory.map((item) => (
        <div className="card" key={item.id}>
          <h3>{item.name}</h3>

          <p>Barcode: {item.barcode}</p>

          <p>Quantity: {item.quantity}</p>

          <p>Price: ${item.price}</p>
        </div>
      ))}

    </div>
  );
}

export default App;