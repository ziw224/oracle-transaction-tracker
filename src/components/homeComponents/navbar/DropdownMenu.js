import React from "react";
import "./navbar.css";
export const DropdownMenu = () => {
  function DropdownItem(props) {
    return (
      <a href="#" className="menu-item">
        <span className="icon-button">{props.leftIcon}</span>
        {props.children}
        <span className="icon-right">{props.rightIcon}</span>
      </a>
    );
  }
  return <div className="dropdown">
    <DropdownItem> user1</DropdownItem>
  </div>;
};
