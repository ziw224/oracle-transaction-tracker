import "./datatable.css";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(
  hashVal: string,
  wallet: string,
  amount: number,
  date: string,
) {
  return { hashVal, wallet, amount, date };
}

const rows = [
  createData('0001', 'usd1qrw038lx5n4wxx3yvuwdndpr7gnm347d6pn37uywgudzq90w7fsuk52kd5u', 25, '10/23'),
];

export const DataTable = () => {
  return (
    <div className="datatable">
        <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>HASH VALUE</TableCell>
            <TableCell align="center">WALLET ADDRESS 2</TableCell>
            <TableCell align="right">TRANSACTION AMOUNT &nbsp;($)</TableCell>
            <TableCell align="right">TRANSACTION DATE</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.hashVal}
              </TableCell>
              <TableCell align="right">{row.wallet}</TableCell>
              <TableCell align="center">{row.amount}</TableCell>
              <TableCell align="center">{row.date}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </div>
  );
};
