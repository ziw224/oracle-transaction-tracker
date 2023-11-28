import React from "react";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import PersonIcon from "@mui/icons-material/Person";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";

import './widget.css'
export const Widget = ({ type }) => {
  let data;
  // temporary: hardcode data for now
  const amount = 100;
  const percentage = 20;

  switch (type) {
    case "user":
      data = {
        title: "USERS",
        isMoney: false,
        link: "See all users",
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
        isMoney: false,
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
          {data.isMoney && "$"} {amount}
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
