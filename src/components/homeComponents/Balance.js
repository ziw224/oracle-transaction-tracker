import React, { useContext, useEffect, useState } from "react";
import { GlobalWalletContext } from "../../context/WalletContext";

export const Balance = () => {
  const { selectedWalletNumber } = useContext(GlobalWalletContext);
  const [balance, setBalance] = useState("0.00");

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        if (selectedWalletNumber) {
          // Fetch the balance
          const balanceResponse = await fetch(`/command/inspect-wallet/${selectedWalletNumber}`);
          const balanceData = await balanceResponse.json();
          const balanceString = balanceData.output[0];
          const balanceMatch = balanceString.match(/Balance: \$(\d+\.\d+)/);
          if (balanceMatch && balanceMatch[1]) {
            setBalance(balanceMatch[1]);
          }
        }
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        setBalance("0.00");
      }
    };

    fetchBalance();
  }, [selectedWalletNumber]);

  return (
    <>
      <h4>Your Balance</h4>
      <h1>${balance}</h1>
    </>
  );
};
