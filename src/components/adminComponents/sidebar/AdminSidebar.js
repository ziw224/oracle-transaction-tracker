import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import PersonIcon from "@mui/icons-material/Person";
import PaymentsIcon from "@mui/icons-material/Payments";
import { Link } from "react-router-dom";

import "./sidebar.css";

export const AdminSidebar = () => {
  return (
    <div className="sidebar">
      <div className="top">
        <span className="logo"> CBDC Admin </span>
      </div>
      <hr />
      <div className="center">
        <ul>
          <p className="title">MAIN</p>
          <Link to="/admin" style={{ textDecoration: "none" }}>
          <li>
            <TrendingUpIcon className="icon" />
            <span>Summary</span>
          </li>
          </Link>
          <p className="title">LISTS</p>
          <Link to="/admin/user" style={{ textDecoration: "none" }}>
            <li>
              <PersonIcon className="icon" />
              <span>Users</span>
            </li>
          </Link>
          <Link to="/admin/payment" style={{ textDecoration: "none" }}>
            <li>
              <PaymentsIcon className="icon" />
              <span>Payment</span>
            </li>
          </Link>
        </ul>
      </div>
    </div>
  );
};

export default AdminSidebar;
