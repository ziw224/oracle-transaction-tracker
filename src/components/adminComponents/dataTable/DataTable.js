import React, { useState, useEffect } from "react";
import { DataGrid } from '@mui/x-data-grid';
import "./datatable.css";

export const DataTable = ({ type }) => {
  const [dataRows, setDataRows] = useState([]);
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      let endpoint = '';
      console.log(type);
      if (type === 'wallets') {
        endpoint = '/cbdc-wallets';
        setColumns([
          { field: 'id', headerName: 'ID', width: 90 },
          { field: 'wallet_number', headerName: 'WALLET NUMBER', width: 150 },
          { field: 'wallet_address', headerName: 'WALLET ADDRESS', width: 250, flex: 1 },
        ]);
      } else if (type === 'transactions' || type === 'transactionholder' || type === 'input' || type === 'output' || type === 'uhspreviews') {
        endpoint = `/table/${type}`;
      }
  
      try {
        const response = await fetch(endpoint, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          },
        });
        const data = await response.json();
  
        if (type === 'wallets') {
          const formattedData = data.wallets.map(wallet => ({
            id: wallet.wallet_number, // Assuming wallet_number is unique and can be used as an id
            ...wallet,
          }));
          setDataRows(formattedData);
        } else {
          setColumns(data.columns.map(column => ({ field: column, headerName: column.toUpperCase() })));
          const formattedData = data.rows.map((row, index) => ({
            id: index, // You might need to adjust this based on how you can uniquely identify rows
            ...row,
          }));
          setDataRows(formattedData);
        }
      } catch (error) {
        console.error(`Failed to fetch ${type} data:`, error);
        setDataRows([]);
      }
    };
  
    fetchData();
  }, [type]);

  return (
    <div className="datatable">
      <DataGrid
        rows={dataRows}
        columns={columns}
        pageSize={5}
        checkboxSelection
        disableSelectionOnClick
        sortingOrder={['asc', 'desc']}
      />
    </div>
  );
};

export default DataTable;
