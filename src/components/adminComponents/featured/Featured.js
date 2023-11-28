import MoreVerrIcon from "@mui/icons-material/MoreVert";
// import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";


import "./featured.css";
export const Featured = () => {
  return (
    <div className="featured">
      <div className="top">
        <h1 className="title">Total Transaction Amount in Dollars</h1>
        <MoreVerrIcon fontsize="small" />
      </div>
      <div className="bottom">
        {/* <div className="featuredChart">
          <CircularProgressbar value={70} text={"70%"} strokWidth={5} />
        </div> */}

        <p className="Bottomtitle">Total transactions made today </p>
        <p className="amount"> Amount: $420 </p>
        <div className="summary">
        <div className="item">
            <div className="item-title">This Week</div>
            <div className="item-result">
              <div className="resultAmount">$12.4K</div>
            </div>
          </div>
          <div className="item">
            <div className="item-title">Last Week</div>
            <div className="item-result">
              <div className="resultAmount">$12.4K</div>
            </div>
          </div>
          <div className="item">
            <div className="item-title">Last Month</div>
            <div className="item-result">
              <div className="resultAmount">$12.4K</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
