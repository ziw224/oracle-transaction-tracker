import React, { useState, useContext, useEffect } from "react";
import { GlobalContext } from "../../context/GlobalState";
import { GlobalWalletContext } from "../../context/WalletContext";

export const AddTransaction = () => {
  const [text, setText] = useState("");
  const [name, setName] = useState(""); // 'name' holds the recipient's wallet address
  const [amount, setAmount] = useState(0);

  const { addTransaction } = useContext(GlobalContext);
  const { selectedWalletNumber } = useContext(GlobalWalletContext); // Get the current user's wallet number
  const [allWallets, setAllWallets] = useState([]);

  useEffect(() => {
    // Fetch all wallets on component mount
    const fetchAllWallets = async () => {
      try {
        const response = await fetch("/cbdc-wallets");
        const data = await response.json();
        setAllWallets(data.wallets);
      } catch (error) {
        console.error("Error fetching wallets:", error);
      }
    };

    fetchAllWallets();
  }, []);

  const findWalletNumber = (address) => {
    const wallet = allWallets.find(w => w.wallet_address === address);
    return wallet ? wallet.wallet_number : null;
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    // Validate input parameters
    if (!name.trim()) {
      alert("Wallet Address is required");
      return;
    }

    if (!amount || isNaN(amount)) {
      alert("Amount must be a valid number");
      return;
    }

    try {
      // Send tokens
      const sendResponse = await fetch(`/command/send-tokens/${selectedWalletNumber}/${amount}/${name}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!sendResponse.ok) {
        throw new Error('Failed to send tokens');
      }

      const sendResult = await sendResponse.json();
      console.log(sendResult);

      // Check if "Data for recipient importinput:" line exists
      const importInputLine = Object.values(sendResult.output).find(line => line.startsWith("Data for recipient importinput:"));
      if (importInputLine) {
        // Extract the token data
        const tokenData = importInputLine.split(":")[1].trim();
        console.log("TOken Data: ", tokenData);

        // Find the wallet number set to
        const recipientWalletNumber = findWalletNumber(name);
        if (recipientWalletNumber) {
          // Make the import tokens call
          const importResponse = await fetch(`/command/import-tokens/${recipientWalletNumber}/${tokenData}`, {
            method: 'GET', // Adjust according to your API specification
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (!importResponse.ok) {
            throw new Error('Failed to import tokens');
          }

          const importResult = await importResponse.json();
          console.log(importResult); // Handle the response as needed
        }
      }

      // Add transaction to the local state (if needed)
      const newTransaction = {
        id: Math.floor(Math.random() * 100000000),
        text,
        name,
        amount: -parseFloat(amount), // Convert amount to a negative number for local state
      };
      addTransaction(newTransaction);

      // Clear input fields after submitting
      setText("");
      setName("");
      setAmount(0);

    } catch (error) {
      console.error("Transaction error:", error);
      alert("Error in transaction: " + error.message);
    }
  };

  return (
    <>
      <h3>Add new transaction</h3>
      <form onSubmit={onSubmit}>
        <div className="form-control">
          <label htmlFor="text">Text</label>
          <input
            type="text"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Enter text..."
          />
        </div>
        <div className="form-control">
          <label htmlFor="user2">Wallet Address</label>
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Enter address..."
          />
        </div>
        <div className="form-control">
          <label htmlFor="amount">Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            placeholder="Enter amount..."
          />
        </div>
        <button className="btn">Add transaction</button>
      </form>
    </>
  );
};
