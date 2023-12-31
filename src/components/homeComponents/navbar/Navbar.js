import React, { useState } from "react";
import "./navbar.css";

export const Navbar = (props) => {
  const [open, setOpen] = useState(false);

  const handleIconClick = (iconType) => {
    if (iconType === "admin") {
      // Handle admin icon click and navigate to the admin page
      window.location.href = "/admin";
    } else {
      // Handle dropdown of users list
      setOpen(!open);
    }
  };

  const toggleDropdown = () => {
    setOpen(!open);
  };

  return (
    <nav className="navbar">
      <ul className="navbar-nav">
        <li className="nav-item">
          {props.icons.map((icon, index) => (
            <div key={index} className="icon-container">
              {icon.type === "admin" && (
                <span className="icon-text">ADMIN</span>
              )}
              {icon.type === "user-list" && (
                <span className="icon-text">USER</span>
              )}
              <a
                href="#!"
                className="icon-button"
                onClick={() => handleIconClick(icon.type)}
              >
                {icon.icon}
              </a>
            </div>
          ))}
          {/* Pass the toggle function to the children */}
          {open && React.cloneElement(props.children, { toggleDropdown })}
        </li>
      </ul>
    </nav>
  );
};
