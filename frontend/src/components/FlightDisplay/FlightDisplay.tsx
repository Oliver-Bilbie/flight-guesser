import { FC, ReactElement, useState } from "react";
import "./FlightDisplay.css";
import { Flight, Points } from "../../utils/types";
import FlightCard from "../FlightCard/FlightCard";
import MapDisplay from "../MapDisplay/MapDisplay";
import PopupMenu from "../PopupMenu/PopupMenu";
import PointsDisplay from "../PointsDisplay/PointsDisplay";
import HideMenu from "../HideMenu/HideMenu";

interface FlightDisplayProps {
  flight: Flight;
  points: Points;
  alreadyGuessed: boolean;
  onClose: () => void;
}

const FlightDisplay: FC<FlightDisplayProps> = ({
  flight,
  points,
  alreadyGuessed,
  onClose: onExit,
}): ReactElement => {
  const [currentView, setCurrentView] = useState(0);

  return (
    <PopupMenu>
      <div className="flight-display">
        <HideMenu isHidden={currentView !== 0}>
          <PointsDisplay
            points={points}
            isAlreadyGuessed={alreadyGuessed}
            hasOrigin={flight.origin !== null}
            hasDestination={flight.destination !== null}
          />
        </HideMenu>
        <HideMenu isHidden={currentView !== 1}>
          <FlightCard flight={flight} />
        </HideMenu>
        <HideMenu isHidden={currentView !== 2}>
          <MapDisplay flight={flight} />
        </HideMenu>

        <div className="flight-display-nav">
          {currentView > 0 && (
            <button onClick={() => setCurrentView(currentView - 1)}>
              {"Back"}
            </button>
          )}

          {currentView < 2 && (
            <button onClick={() => setCurrentView(currentView + 1)}>
              {"Next"}
            </button>
          )}

          {currentView === 2 && (
            <button onClick={() => onExit()}>{"Done"}</button>
          )}
        </div>
      </div>
    </PopupMenu>
  );
};

export default FlightDisplay;
