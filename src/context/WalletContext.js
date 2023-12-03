import React, { createContext, useState } from 'react';

export const GlobalWalletContext = createContext();

export const GlobalWalletProvider = ({ children }) => {
  const [selectedWalletNumber, setSelectedWalletNumber] = useState(null);

  return (
    <GlobalWalletContext.Provider value={{ selectedWalletNumber, setSelectedWalletNumber }}>
      {children}
    </GlobalWalletContext.Provider>
  );
};
