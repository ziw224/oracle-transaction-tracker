import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Wallet } from "./pages/wallet/Wallet";
import { Admin } from "./pages/admin/Admin";
import { List } from "./pages/admin/list/List";

import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Wallet />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/admin/user" element={<List type="wallets" />} />
          <Route path="/admin/payment" element={<List type="transactions" />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
