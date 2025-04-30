import { FC, ReactElement } from "react";
import "./LoadingSpinner.css";
import spinnerImg from "../../assets/aircraft.webp";

const LoadingSpinner: FC = (): ReactElement => {
  return (
    <div className="loading-spinner">
      <div className="loading-spinner-container">
        <img
          src={spinnerImg}
          alt="Loading..."
          className="loading-spinner-image"
        />
      </div>
    </div>
  );
};

export default LoadingSpinner;
