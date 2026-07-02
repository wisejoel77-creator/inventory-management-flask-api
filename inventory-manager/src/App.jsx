import { useEffect, useState } from "react";
import "./App.css";

function App() {

  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/inventory")
      .then((response) => response.json())
      .then((data) => {
        setInventory(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div className="container">

      <h1>Inventory Management System</h1>

      <h2>Current Inventory</h2>

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