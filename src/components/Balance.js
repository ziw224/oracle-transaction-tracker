import React, { useContext } from "react";
import { GlobalContext } from "../context/GlobalState";


export const Balance = () => {
  const { transactions } = useContext(GlobalContext);
  
  // Mapping through and getting all the amounts in the history
  const amounts = transactions.map(transaction => transaction.amount);
  
  // Adding them all together and keeping two decimal places.
  const total = amounts.reduce((acc, item) => (acc += item), 0).toFixed(2);
  
  return (
    <>
      <h4>Your Balance</h4>
      <h1> {total} </h1>
    </>
  );
};
