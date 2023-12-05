import { Header } from "../../components/homeComponents/Header";
import { Balance } from "../../components/homeComponents/Balance";
import { InputOutput } from "../../components/homeComponents/InputOutput";
import { TransactionList } from "../../components/homeComponents/TransactionList";
import { AddTransaction } from "../../components/homeComponents/AddTransaction";
import { Navbar } from "../../components/homeComponents/navbar/Navbar";
import { DropdownMenu } from "../../components/homeComponents/navbar/DropdownMenu";
import { GlobalProvider } from "../../context/GlobalState";
import "../../App.css";

export const Home = () => {


  return (
    <GlobalProvider>
      <Navbar>
        <DropdownMenu/>
      </Navbar>
      <Header />
      <div className="container">
        <Balance />
        <InputOutput />
        <TransactionList />
        <AddTransaction />
      </div>
    </GlobalProvider>
  );
};
export default Home;
