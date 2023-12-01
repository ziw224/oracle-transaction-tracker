import "./list.css";
import { AdminSidebar } from "../../../components/adminComponents/sidebar/AdminSidebar";
import { DataTable } from "../../../components/adminComponents/dataTable/DataTable";

export const List = ({ type }) => {       // Accept the 'type' prop here
  return (
    <div className="admin-list">
      <AdminSidebar />
      <div className="listContainer">
        <DataTable type={type} /> {/* Pass the 'type' prop to DataTable */}
      </div>
    </div>
  );
};

export default List;
