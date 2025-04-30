import { FC, ReactElement, useState } from "react";
import "./FlightDisplay.css";
import { Flight, Points } from "../../utils/types";
import FlightCard from "../FlightCard/FlightCard";
import MapDisplay from "../MapDisplay/MapDisplay";
import PopupMenu from "../PopupMenu/PopupMenu";
import PointsDisplay from "../PointsDisplay/PointsDisplay";

interface FlightDisplayProps {
  flight: Flight;
  points: Points;
  onClose: () => void;
}

const FlightDisplay: FC<FlightDisplayProps> = ({
  flight,
  points,
  onClose: onExit,
}): ReactElement => {
  const [currentView, setCurrentView] = useState(0);

  const dataViews = [
    <PointsDisplay points={points} />,
    <FlightCard flight={flight} />,
    <MapDisplay flight={flight} />,
  ];

  return (
    <PopupMenu>
      <div className="flight-display">
        {dataViews[currentView]}

        <div className="flight-display-nav">
          {currentView > 0 && (
            <button onClick={() => setCurrentView(currentView - 1)}>
              {"Back"}
            </button>
          )}

          {currentView + 1 < dataViews.length && (
            <button onClick={() => setCurrentView(currentView + 1)}>
              {"Next"}
            </button>
          )}

          {currentView + 1 === dataViews.length && (
            <button onClick={() => onExit()}>{"Done"}</button>
          )}
        </div>
      </div>
    </PopupMenu>
  );
};

export default FlightDisplay;
