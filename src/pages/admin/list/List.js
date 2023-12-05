import "./list.css";
import { AdminSidebar } from "../../../components/adminComponents/sidebar/AdminSidebar";
import { DataTable } from "../../../components/adminComponents/dataTable/DataTable";

export const List = ({ type }) => {
  const handleButtonClick = async () => {
    try {
      const response = await fetch('/command/new-wallet', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  };

  return (
    <div className="admin-list">
      <AdminSidebar />
      <div className="listContainer">
        <div className="dataTableContainer">
          <DataTable type={type} />
          <button onClick={handleButtonClick} className="fetchButton">New User</button> {/* Add your button here */}
        </div>
      </div>
    </div>
  );
};

export default List;
