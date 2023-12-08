import React, { useContext } from "react";


export const Transaction = ({transaction}) => {
    
    const sign = transaction.amount < 0 ? '-' : '+';

    const transactionType = transaction.amount < 0 ? 'to' : 'from';

    return (
    <li className={transaction.amount < 0 ? 'minus' : 'plus'}>
      {/* <span>{transaction.id}</span> {transaction.text} <span>{sign}{Math.abs(transaction.amount)}</span> {transactionType} {transaction.name} */}
      <span></span> <span>{sign}{Math.abs(transaction.amount)}</span> {transactionType} {transaction.name}
    </li>
  );
};

