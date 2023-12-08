import React from "react";

export const Transaction = ({ transaction }) => {
  const sign = transaction.amount < 0 ? '-' : '+';
  const transactionType = transaction.amount < 0 ? 'to' : 'from';

  // Truncate transaction.name to the first 15 characters and add '...'
  const truncatedName = transaction.name.length > 15
    ? transaction.name.substring(0, 15) + '...'
    : transaction.name;

  return (
    <li className={transaction.amount < 0 ? 'minus' : 'plus'}>
      <span></span>
      <span>{sign}{Math.abs(transaction.amount)}</span>
      {transactionType} {truncatedName}
    </li>
  );
};
