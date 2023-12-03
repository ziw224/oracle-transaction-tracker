import React, { useContext, useEffect, useState } from "react";
import { GlobalWalletContext } from "../../context/WalletContext";

export const Balance = () => {
  const { selectedWalletNumber } = useContext(GlobalWalletContext);
  const [balance, setBalance] = useState("0.00");
  const [spent, setSpent] = useState("0.00"); // If you need to display spent here as well

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

          // Fetch the spent value
          // Replace this URL with your actual endpoint for fetching the spent value
          const spentResponse = "0.00";
          setSpent(spentResponse);
        }
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        setBalance("0.00");
        // Handle error for spent value as well
        setSpent("0.00");
      }
    };

    fetchBalance();
  }, [selectedWalletNumber]);

  return (
    <>
      <h4>Your Balance</h4>
      <h1>${balance}</h1>
      {/* Display spent value if necessary */}
      <h4>Spent</h4>
      <h1>${spent}</h1>
    </>
  );
};
