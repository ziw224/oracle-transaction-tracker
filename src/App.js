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
          <Route path="/">
            <Route index element={<Home />} />
            <Route path="/admin">
              <Route index element={<Admin />} />
            </Route>
            <Route path="/admin/user" >
              <Route index element={<List />} />
            </Route>
            <Route path="/admin/payment">
              <Route index element={<List />} />
            </Route>
          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
