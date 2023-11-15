import React, { useState, useContext } from "react";
import { GlobalContext } from "../context/GlobalState";

export const AddTransaction = () => {

  const [text, setText] = useState("");
  const [name, setName] = useState("");
  const [amount, setAmount] = useState(0);

  const {addTransaction} = useContext(GlobalContext);
  
  const onSubmit = e => {
    e.preventDefault();
    const newTransaction = {
      id: Math.floor(Math.random()*100000000),
      text,
      name,
      amount: +amount // turing "amount" into a number
    }
    addTransaction(newTransaction);
  }


  return (
    <>
      <h3>Add new transaction</h3>
      <form onSubmit = {onSubmit}>
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
          <label htmlFor="user2">User2</label>
          <input
            type="user2"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Enter user name..."
          />
        </div>
        <div className="form-control">
          <label htmlFor="amount">
            Amount <br />
            (negative - expense, positive - income)
          </label>
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
