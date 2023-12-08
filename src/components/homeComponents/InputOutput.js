import React, { useContext, useEffect, useState } from "react";
import { GlobalWalletContext } from "../../context/WalletContext";

export const InputOutput = () => {
  const { selectedWalletNumber } = useContext(GlobalWalletContext);
  const [unspent, setUnspent] = useState("0.00");
  const [spent, setSpent] = useState("0.00");

  useEffect(() => {
    const fetchUTXOs = async () => {
      if (selectedWalletNumber) {
        try {
          const response = await fetch(`/command/inspect-wallet/${selectedWalletNumber}`);
          const data = await response.json();
          const utxoString = data.output[0];
          const utxoMatch = utxoString.match(/UTXOs: (\d+)/);
          if (utxoMatch && utxoMatch[1]) {
            setUnspent(utxoMatch[1]); // Set the number of UTXOs
          }
          // For the spent value, you would typically have a different endpoint or logic to fetch this data.
          // Here I'm assuming you have another endpoint or already have the data in your context.
          // You should replace the below fetch or calculation for 'spent' as per your application logic.
          const spentResponse = "0.00";
          setSpent(spentResponse);
        } catch (error) {
          console.error("Failed to fetch UTXOs:", error);
          setUnspent("0.00");
          setSpent("0.00");
        }
      }
    };

    fetchUTXOs();
  }, [selectedWalletNumber]);

  return (
    <div className="inc-exp-container">
      <div>
        <h4>Unspent</h4>
        <p className="money plus"> {unspent} </p>
      </div>
      <div>
        <h4>Spent</h4>
        <p className="money minus"> {spent} </p>
      </div>
    </div>
  );
};
