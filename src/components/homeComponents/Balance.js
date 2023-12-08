import React, { useContext, useEffect, useState } from "react";
import { GlobalWalletContext } from "../../context/WalletContext";

export const Balance = () => {
  const { selectedWalletNumber } = useContext(GlobalWalletContext);
  const [balance, setBalance] = useState("0.00");
  const [walletAddress, setWalletAddress] = useState("");

  useEffect(() => {
    const fetchWalletData = async () => {
      try {
        const walletsResponse = await fetch("/cbdc-wallets");
        const walletsData = await walletsResponse.json();

        const selectedWallet = walletsData.wallets.find(wallet => wallet.wallet_number === selectedWalletNumber);
        if (selectedWallet) {
          setWalletAddress(selectedWallet.wallet_address);

          const balanceResponse = await fetch(`/command/inspect-wallet/${selectedWalletNumber}`);
          const balanceData = await balanceResponse.json();
          const balanceString = balanceData.output[0];
          const balanceMatch = balanceString.match(/Balance: \$(\d+\.\d+)/);
          if (balanceMatch && balanceMatch[1]) {
            setBalance(balanceMatch[1]);
          }
        } else {
          setWalletAddress("Not Found");
          setBalance("0.00");
        }
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        setWalletAddress("");
        setBalance("0.00");
      }
    };

    if (selectedWalletNumber) {
      fetchWalletData();
    }
  }, [selectedWalletNumber]);

  return (
    <>
      <h4>Your Balance</h4>
      <h1>${balance}</h1>
      {walletAddress && (
        <>
          <h4>Wallet Address</h4>
          <p>{walletAddress}</p>
        </>
      )}
    </>
  );
};
