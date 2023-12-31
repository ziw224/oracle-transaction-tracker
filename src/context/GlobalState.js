import React, { createContext, useReducer } from "react";
import AppReducer from "./AppReducer";

// initial state
const initialState = {
  transactions: [],
};

// const fetchData = async () => {
//   try {
//     const response = await fetch("/table/test", {
//       method: "GET",
//       headers: { Accept: "application/json" },
//     });
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
//     const data = await response.json();
//     return data.rows || [];
//   } catch (error) {
//     console.error("Error fetching data:", error);
//     return [];
//   }
// };

// Create context
export const GlobalContext = createContext(initialState);

// Provider component
export const GlobalProvider = ({ children }) => {
  const [state, dispatch] = useReducer(AppReducer, initialState);

  // // Fetch data and set it as the initial state
  // useEffect(() => {
  //   const fetchInitialData = async () => {
  //     const initialData = await fetchData();
  //     // Dispatch an action to set the initial state
  //     dispatch({
  //       type: "SET_INITIAL_STATE",
  //       payload: initialData,
  //     });
  //   };

  //   fetchInitialData();
  // }, []); // The empty dependency array ensures this effect runs only once on mount

  // Actions
  function addTransaction(transaction) {
    dispatch({
      type: "ADD_TRANSACTION",
      payload: transaction,
    });
  }

  return (
    <GlobalContext.Provider
      value={{
        transactions: state.transactions,
        addTransaction,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};