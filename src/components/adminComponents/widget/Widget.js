import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
// import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import PersonIcon from "@mui/icons-material/Person";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import "./widget.css";

export const Widget = ({ type }) => {
  const [userCount, setUserCount] = useState(0); // Initialize user count to 0
  const [transactionAmount, setTransactionAmount] = useState(null); // Placeholder for transaction amount
  // let percentage = 20
  
  useEffect(() => {
    const fetchWalletData = async () => {
      try {
        const response = await fetch("/cbdc-wallets");
        const data = await response.json();
        if (data.wallets && data.wallets.length > 0) {
          const lastWallet = data.wallets[data.wallets.length - 1];
          setUserCount(lastWallet.wallet_number);
        } else {
          setUserCount(0); // Set user count to 0 if there are no wallets
        }
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        setUserCount(0); // Consider setting user count to 0 in case of an error
      }
    };

    setTransactionAmount(100); // Placeholder value

    fetchWalletData();
  }, []); // Dependency array is empty, so this effect runs once on mount

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
            className="widget-icon"
            style={{ color: "crimson", backgroundColor: "rgba(255,0,0,0.2)" }}
          />
        ),
      };
      break;
    case "transactions":
      data = {
        title: "OVERALL TRANSACTIONS (NUMBER IN TOTAL)",
        isMoney: false,
        link: (
          <Link to="/admin/payment" className="link">
            View all transactions
          </Link>
        ),
        icon: (
          <AccountBalanceIcon
            className="widget-icon"
            style={{ backgroundColor: "rgba(128,0,128,0.2)", color: "purple" }}
          />
        ),
      };
      break;
    default:
      data = {
        title: "Unknown",
        isMoney: false,
        link: <span>{type}</span>,
        icon: <div />, // or any default icon
      };
      break;
  }

  return (
    <div className="widget">
      <div className="left">
        <span className="widget-title">{data.title}</span>
        <span className="counter">
          {data.isMoney && "$"}{" "}
          {type === "user" ? userCount : transactionAmount}
        </span>
        <span className="link">{data.link}</span>
      </div>
      <div className="left">
        {/* <div className="percentage positive">
          <KeyboardArrowUpIcon />
          {percentage}%
        </div> */}
        {data.icon}
      </div>
    </div>
  );
};

export default Widget;
