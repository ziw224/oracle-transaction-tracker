import "./list.css";
import { AdminSidebar } from "../../../components/adminComponents/sidebar/AdminSidebar";
import { DataTable } from "../../../components/adminComponents/dataTable/DataTable";

export const List = () => {
  return (
    <div className="list">
      <AdminSidebar />
      <div className="listContainer">
        <DataTable />
      </div>
    </div>
  );
};

export default List;