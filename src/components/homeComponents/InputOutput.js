import React, { useContext, useEffect, useState } from "react";
import { GlobalWalletContext } from "../../context/WalletContext";

export const InputOutput = () => {
  const { selectedWalletNumber } = useContext(GlobalWalletContext);
  const [unspent, setUnspent] = useState("0.00");
  const [spent, setSpent] = useState("0.00");

  useEffect(() => {
    const fetchData = async () => {
      if (selectedWalletNumber) {
        try {
          // Fetch UTXOs
          const response = await fetch(`/command/inspect-wallet/${selectedWalletNumber}`);
          const data = await response.json();
          const utxoString = data.output[0];
          const utxoMatch = utxoString.match(/UTXOs: (\d+)/);
          if (utxoMatch && utxoMatch[1]) {
            setUnspent(utxoMatch[1]); // Set the number of UTXOs
          }

          // Fetch spent value
          // Replace the below URL with your actual endpoint for fetching the spent value
          const spentResponse = "0.00";
          setSpent(spentResponse);

        } catch (error) {
          console.error("Failed to fetch wallet data:", error);
          setUnspent("0.00");
          // Handle error for spent value as well
          setSpent("0.00");
        }
      }
    };

    fetchData();
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
