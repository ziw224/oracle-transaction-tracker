import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import PersonIcon from "@mui/icons-material/Person";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import './widget.css';

export const Widget = ({ type }) => {
  const [userCount, setUserCount] = useState(null); // State to hold the user count
  const [transactionAmount, setTransactionAmount] = useState(null); // Placeholder for transaction amount
  const percentage = 20; // Assuming this is static for now

  // Suppose you also want to fetch the transaction amount, you would add it here
  useEffect(() => {
    // Fetch the wallet data from the server
    const fetchWalletData = async () => {
      try {
        const response = await fetch('/cbdc-wallets');
        const data = await response.json();
        const lastWallet = data.wallets[data.wallets.length - 1];
        setUserCount(lastWallet.wallet_number); // Update the user count state
        // You would replace this with actual logic to fetch transaction amount
        setTransactionAmount(100); // Placeholder value
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
      }
    };

    fetchWalletData();
  }, []); // Empty dependency array means this effect runs once on mount

  let data;
  switch (type) {
    case "user":
      data = {
        title: "USERS",
        isMoney: false,
        link: (
          <Link to="/admin/user" className="link">
            See all users
          </Link>
        ),
        icon: (
          <PersonIcon
            className="icon"
            style={{ color: "crimson", backgroundColor: "rgba(255,0,0,0.2)" }}
          />
        ),
      };
      break;
    case "transaction":
      data = {
        title: "OVERALL TRANSACTIONS",
        isMoney: true, // Assuming you want to display money for transactions
        link: "View all transactions",
        icon: (
          <AccountBalanceIcon
            className="icon"
            style={{ backgroundColor: "rgba(128,0,128,0.2)", color: "purple" }}
          />
        ),
      };
      break;
    default:
      break;
  }

  return (
    <div className="widget">
      <div className="left">
        <span className="title">{data.title}</span>
        <span className="counter">
          {data.isMoney && "$"} {type === "user" ? userCount : transactionAmount}
        </span>
        <span className="link">{data.link}</span>
      </div>
      <div className="left">
        <div className="percentage positive">
          <KeyboardArrowUpIcon />
          {percentage}%
        </div>
        {data.icon}
      </div>
    </div>
  );
};

export default Widget;
