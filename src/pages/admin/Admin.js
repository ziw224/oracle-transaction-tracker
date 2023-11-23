import { AdminSidebar } from "../../components/sidebar/AdminSidebar";
import { Navbar } from "../../components/navbar/Navbar";
import { Widget } from "../../components/widget/Widget";
import "../../App.css";

export const Admin = () => {
  return (
    <div className="admin">
      <AdminSidebar />
      <div className="homeContainer">
        <Navbar />
        <div className="widgets">
          <Widget type="user" />
          <Widget type="transaction" />
        </div>

      </div>
    </div>
  );
};

export default Admin;
