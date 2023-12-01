import React, { useState, useEffect } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import "./datatable.css";

export const DataTable = () => {
  const [wallets, setWallets] = useState([]);

  useEffect(() => {
    // Fetch the wallet data from the server
    const fetchWalletData = async () => {
      try {
        const response = await fetch('/cbdc-wallets'); // This is the endpoint to fetch wallets
        const data = await response.json();
        setWallets(data.wallets); // Set the wallets state with the fetched data
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
        // Handle error state here
      }
    };

    fetchWalletData();
  }, []); // Dependency array is empty, so the effect runs once on mount

  return (
    <div className="datatable">
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="a dense table">
          <TableHead>
            <TableRow>
              <TableCell>WALLET NUMBER</TableCell>
              <TableCell>WALLET ADDRESS</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {wallets.map((wallet) => (
              <TableRow key={wallet.wallet_number}>
                <TableCell component="th" scope="row">
                  {wallet.wallet_number}
                </TableCell>
                <TableCell>{wallet.wallet_address}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default DataTable;
