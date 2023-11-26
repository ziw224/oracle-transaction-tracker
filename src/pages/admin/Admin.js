import { AdminSidebar } from "../../components/adminComponents/sidebar/AdminSidebar";
import { Widget } from "../../components/adminComponents/widget/Widget";
import { Featured } from "../../components/adminComponents/featured/Featured";
import { Chart } from "../../components/adminComponents/chart/Chart";
import "../../App.css";

export const Admin = () => {
  return (
    <div className="admin">
      <AdminSidebar />
      <div className="homeContainer">
        <div className="widgets">
          <Widget type="user" />
          <Widget type="transaction" />
        </div>
        <div className="charts">
           <Featured />
           <Chart />
        </div>
      </div>
    </div>
  );
};

export default Admin;
