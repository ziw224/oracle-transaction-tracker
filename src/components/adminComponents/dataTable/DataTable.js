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
          { field: 'wallet_number', headerName: 'WALLET NUMBER' },
          { field: 'wallet_address', headerName: 'WALLET ADDRESS' },
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
          setDataRows(data.wallets);
        } else {
          setColumns(data.columns.map(column => ({ field: column, headerName: column })));
          setDataRows(data.rows);
        }
      } catch (error) {
        console.error(`Failed to fetch ${type} data:`, error);
        setDataRows([]);
      }
    };

    fetchData();
  }, [type]); // Dependency array includes type, so the effect will re-run if type changes

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
