import React from "react";
import FaceIcon from '@mui/icons-material/Face';

import "./navbar.css";


export const DropdownMenu = () => {
  function DropdownItem(props) {
    return (
      <a className="menu-item">
        <span className="icon-button">{props.leftIcon}</span>
        {props.children}
      </a>
    );
  }
  return (
    <div className="dropdown">
      <DropdownItem leftIcon={<FaceIcon/>}>user1</DropdownItem>
      <DropdownItem leftIcon={<FaceIcon/>}>user2</DropdownItem>
      <DropdownItem leftIcon={<FaceIcon/>}>user3</DropdownItem>
    </div>
  );
};
