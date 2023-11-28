import { Header } from "../../components/homeComponents/Header";
import { Balance } from "../../components/homeComponents/Balance";
import { InputOutput } from "../../components/homeComponents/InputOutput";
import { TransactionList } from "../../components/homeComponents/TransactionList";
import { AddTransaction } from "../../components/homeComponents/AddTransaction";
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
