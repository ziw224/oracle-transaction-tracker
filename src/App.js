import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Wallet } from "./pages/wallet/Wallet";
import { Admin } from "./pages/admin/Admin";
import { List } from "./pages/admin/list/List";
import { GlobalWalletProvider } from './context/WalletContext';

import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <GlobalWalletProvider>
          <Routes>
            <Route path="/" element={<Wallet />} />
            <Route path="/admin" element={<Admin />} />
            <Route path="/admin/user" element={<List type="wallets" />} />
            <Route path="/admin/payment" element={<List type="transactions" />} />
          </Routes>
        </GlobalWalletProvider>
      </Router>
    </div>
  );
}

export default App;
