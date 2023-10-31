import { Header } from "./components/Header";
import { Balance } from "./components/Balance";
import { InputOutput } from "./components/InputOutput";

import "./App.css";

function App() {
  return (
    <div>
      <Header />
      <div className="container">
        <Balance />
        <InputOutput />
      </div>
    </div>
  );
}

export default App;
