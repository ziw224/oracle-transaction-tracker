import React, { useState } from "react";
import ArrowDropDownCircleIcon from "@mui/icons-material/ArrowDropDownCircle";
import "./navbar.css";
export const Navbar = (props) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="navbar">
        <div className="nav-item">
          <ArrowDropDownCircleIcon
            href="#"
            className="icon-button"
            onClick={() => setOpen(!open)}
          >
            {" "}
            {props.icon}
          </ArrowDropDownCircleIcon>
        </div>
      {open && props.children}
    </div>
  );
};
