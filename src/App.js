// import { Header } from "./components/Header";
// import { Balance } from "./components/Balance";
// import { InputOutput } from "./components/InputOutput";
// import { TransactionList } from "./components/TransactionList";
// import { AddTransaction } from "./components/AddTransaction";
// import { GlobalProvider } from "./context/GlobalState";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Home from "./pages/home/Home";
import Admin from "./pages/admin/Admin";

import "./App.css";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/">
            <Route index element={<Home/>} />
            <Route path="admin" element={<Admin/>} />
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
