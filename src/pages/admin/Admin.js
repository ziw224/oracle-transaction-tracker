import { AdminSidebar } from "../../components/adminComponents/sidebar/AdminSidebar";
import { Widget } from "../../components/adminComponents/widget/Widget";
import { Featured1 } from "../../components/adminComponents/featured/featured1/Featured1";
import { Featured2 } from "../../components/adminComponents/featured/featured2/Featured2";
import { Chart1 } from "../../components/adminComponents/chart/chart1/Chart1";
import { Chart2 } from "../../components/adminComponents/chart/chart2/Chart2";
import "../../App.css";

export const Admin = () => {
  return (
    <div className="admin">
      <AdminSidebar />
      <div className="homeContainer">
        <div className="widgets">
          <Widget type="user" />
          <Widget type="transactions" />
        </div>
        <div className="charts">
          <Featured1 />
          <Chart1 />
        </div>
        <div className="charts">
           <Featured2 />
           <Chart2 />
        </div>
      </div>
    </div>
  );
};

export default Admin;
