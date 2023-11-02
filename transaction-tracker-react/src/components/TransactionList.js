import React, { useContext } from "react";
import { GlobalContext } from "../context/GlobalState";

export const TransactionList = () => {
  const { transactions } = useContext(GlobalContext);
  return (
    <div>
      <h3>History</h3>
      <ul className="list">
        {transactions.map((transactions) => (
          <li className="minus">
            {transactions.text} <span>-400</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
