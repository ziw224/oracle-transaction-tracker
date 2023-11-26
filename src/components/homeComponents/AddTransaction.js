import React, { useState, useContext } from "react";
import { GlobalContext } from "../../context/GlobalState";

export const AddTransaction = () => {
  const [text, setText] = useState("");
  const [name, setName] = useState("");
  const [amount, setAmount] = useState();

  const { addTransaction } = useContext(GlobalContext);

  const onSubmit = (e) => {
    e.preventDefault();

    // Validate input parameters
    if (!name.trim()) {
      alert("Wallet Address is required");
      return;
    }

    if (!amount || isNaN(amount)) {
      alert("Amount must be a valid number");
      return;
    }

    const newTransaction = {
      id: Math.floor(Math.random() * 100000000),
      text,
      name,
      amount: -parseFloat(amount), // Convert amount to a negative number
    };

    addTransaction(newTransaction);

    // Clear input fields after submitting
    setText("");
    setName("");
    setAmount(0);
  };

  return (
    <>
      <h3>Add new transaction</h3>
      <form onSubmit={onSubmit}>
        <div className="form-control">
          <label htmlFor="text">Text</label>
          <input
            type="text"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Enter text..."
          />
        </div>
        <div className="form-control">
          <label htmlFor="user2">Wallet Address</label>
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Enter address..."
          />
        </div>
        <div className="form-control">
          <label htmlFor="amount">Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            placeholder="Enter amount..."
          />
        </div>
        <button className="btn">Add transaction</button>
      </form>
    </>
  );
};
