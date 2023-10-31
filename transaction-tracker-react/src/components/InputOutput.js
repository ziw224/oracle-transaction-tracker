import React from "react";

export const InputOutput = () => {
  return (
    <div class="inc-exp-container">
      <div>
        <h4>Spent</h4>
        <p id="money-plus" class="money plus">
          +$0.00
        </p>
      </div>
      <div>
        <h4>Unspent</h4>
        <p id="money-minus" class="money minus">
          -$0.00
        </p>
      </div>
    </div>
  );
};
