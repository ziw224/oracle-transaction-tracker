import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PersonIcon from '@mui/icons-material/Person';
import PaymentsIcon from '@mui/icons-material/Payments';

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
          <li>
            <TrendingUpIcon className="icon"/>
            <span>Summary</span>
          </li>
          <p className="title">LISTS</p>
          <li>
            <PersonIcon className="icon"/>
            <span>Users</span>
          </li>
          <li>
            <PaymentsIcon className="icon"/>
            <span>Payment</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default AdminSidebar;
