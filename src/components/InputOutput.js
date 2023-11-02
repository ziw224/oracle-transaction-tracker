import React from "react";

export const InputOutput = () => {
  return (
    <div className ="inc-exp-container">
      <div>
        <h4>Unspent</h4>
        <p className ="money plus">
          +$0.00
        </p>
      </div>
      <div>
        <h4>Spent</h4>
        <p className ="money minus">
          -$0.00
        </p>
      </div>
    </div>
  );
};
