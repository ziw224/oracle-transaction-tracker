import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home } from "./pages/home/Home";
import { Admin } from "./pages/admin/Admin";
import { List } from "./pages/admin/list/List";

import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/admin/user" element={<List type="wallets" />} />
          <Route path="/admin/payment" element={<List type="transactions" />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
