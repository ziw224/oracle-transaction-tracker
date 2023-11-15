import { Header } from "../../components/Header";
import { Balance } from "../../components/Balance";
import { InputOutput } from "../../components/InputOutput";
import { TransactionList } from "../../components/TransactionList";
import { AddTransaction } from "../../components/AddTransaction";
import { GlobalProvider } from "../../context/GlobalState";
import "../../App.css";

export const Home = () => {
    return (
        <GlobalProvider>
          <Header />
          <div className="container">
            <Balance />
            <InputOutput />
            <TransactionList />
            <AddTransaction />
          </div>
        </GlobalProvider>
      );
}

export default Home;
