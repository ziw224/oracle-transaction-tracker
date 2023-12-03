import React, { useEffect, useState } from "react";
import FaceIcon from '@mui/icons-material/Face';
import "./navbar.css";

export const DropdownMenu = () => {
  const [wallets, setWallets] = useState([]);
  const [selectedWalletNumber, setSelectedWalletNumber] = useState(null);

  useEffect(() => {
    const fetchWalletData = async () => {
      try {
        const response = await fetch("/cbdc-wallets");
        const data = await response.json();
        if (data.wallets && data.wallets.length > 0) {
          setWallets(data.wallets);
        } else {
          setWallets([]); // Set to empty array if there are no wallets
        }
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        setWallets([]); // Set to empty array in case of an error
      }
    };

    fetchWalletData();
  }, []);
  
  function DropdownItem(props) {
    // Add onClick handler to set selected wallet
    return (
      <a className={`menu-item ${props.walletNumber === selectedWalletNumber ? 'selected' : ''}`}
         onClick={() => setSelectedWalletNumber(props.walletNumber)}>
        <span className="icon-button">{props.leftIcon}</span>
        {props.children}
      </a>
    );
  }

  return (
    <div className="dropdown">
      {wallets.map((wallet) => (
        <DropdownItem 
          leftIcon={<FaceIcon />} 
          key={wallet.wallet_number} 
          walletNumber={wallet.wallet_number}
        >
          User {wallet.wallet_number}
        </DropdownItem>
      ))}
    </div>
  );
};