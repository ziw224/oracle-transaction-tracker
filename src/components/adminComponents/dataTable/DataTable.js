import React, { useState, useEffect } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
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
        setColumns(['WALLET NUMBER', 'WALLET ADDRESS']);
      } else if (type === 'transactions') {
        endpoint = '/table/transaction';
      } else if (type === 'transactionholder') {
        endpoint = '/table/transactionholder';
      } else if (type === 'input') {
        endpoint = '/table/input';
      } else if (type === 'output') {
        endpoint = '/table/output';
      } else if (type === 'uhspreviews') {
        endpoint = '/table/uhspreviews';
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
          setDataRows(data.wallets.map(wallet => ({
            wallet_number: wallet.wallet_number,
            wallet_address: wallet.wallet_address
          })));
        } else if (type === 'transactions') {
          setColumns(data.columns);
          setDataRows(data.rows);
        } else if (type === 'transactionholder') {
          setColumns(data.columns);
          setDataRows(data.rows);
        } else if (type === 'input') {
          setColumns(data.columns);
          setDataRows(data.rows);
        } else if (type === 'output') {
          setColumns(data.columns);
          setDataRows(data.rows);
        } else if (type === 'uhspreviews') {
          setColumns(data.columns);
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
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="a dense table">
          <TableHead>
            <TableRow>
              {columns.map((column, index) => (
                <TableCell key={index}>{column}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {dataRows.map((row, index) => (
              <TableRow key={index}>
                {Object.values(row).map((value, cellIndex) => (
                  <TableCell key={cellIndex}>
                    {value !== null ? value : 'N/A'}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default DataTable;
