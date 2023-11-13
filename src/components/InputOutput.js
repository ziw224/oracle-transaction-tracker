import React, { useContext } from "react";
import { GlobalContext } from "../context/GlobalState";

export const InputOutput = () => {
  const { transactions } = useContext(GlobalContext);

  const amounts = transactions.map((transaction) => transaction.amount);

  // Total of Unspent tokens (considering it as an income or output )
  const unspent = amounts
    .filter((item) => item > 0)
    .reduce((acc, item) => (acc += item), 0)
    .toFixed(2);

  // Total of Spent tokents (considering it as an expense of input)
  const spent = (
    amounts.filter((item) => item < 0).reduce((acc, item) => (acc += item), 0) *
    -1
  ).toFixed(2);
  return (
    <div className="inc-exp-container">
      <div>
        <h4>Unspent</h4>
        <p className="money plus"> {unspent}</p>
      </div>
      <div>
        <h4>Spent</h4>
        <p className="money minus">{spent}</p>
      </div>
    </div>
  );
};
