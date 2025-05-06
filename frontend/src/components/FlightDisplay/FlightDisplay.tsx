import { FC, ReactElement, useState } from "react";
import "./FlightDisplay.css";
import FlightCard from "../FlightCard/FlightCard";
import HideMenu from "../HideMenu/HideMenu";
import MapDisplay from "../MapDisplay/MapDisplay";
import MessageDisplay from "../MessageDisplay/MessageDisplay";
import PointsDisplay from "../PointsDisplay/PointsDisplay";
import { useGameStore } from "../../utils/gameStore";
import { useLobbyStore } from "../../utils/lobbyStore";

interface FlightDisplayProps {
  onClose: () => void;
}

const FlightDisplay: FC<FlightDisplayProps> = ({ onClose }): ReactElement => {
  const [currentView, setCurrentView] = useState(0);

  const singleRules = useGameStore((state) => state.rules);
  const singleResponse = useGameStore((state) => state.response);

  const isMultiplayer = useLobbyStore((state) => state.isActive);
  const multiRules = useLobbyStore((state) => state.rules);
  const multiResponse = useLobbyStore((state) => state.response);

  const currentResponse = isMultiplayer ? multiResponse : singleResponse;
  const currentRules = isMultiplayer ? multiRules : singleRules;

  // We must clone the state at the time the guess was made to avoid confusion if anything changes later
  const [response] = useState(() => structuredClone(currentResponse));
  const [rules] = useState(() => structuredClone(currentRules));

  if (response.value === null) {
    return (
      <MessageDisplay
        title="No flight data available"
        message="There is no current flight data to display"
        continueText="Back"
        onContinue={() => onClose()}
      />
    );
  }

  if (rules === null) {
    return (
      <MessageDisplay
        title="No rules data available"
        message="There is no rules data available, so it was not possible to display the flight"
        continueText="Back"
        onContinue={() => onClose()}
      />
    );
  }

  return (
    <div className="flight-display">
      <HideMenu isHidden={currentView !== 0}>
        <PointsDisplay
          points={response.value.points}
          status={response.status}
          rules={rules}
        />
      </HideMenu>
      <HideMenu isHidden={currentView !== 1}>
        <FlightCard flight={response.value.flight} />
      </HideMenu>
      <HideMenu isHidden={currentView !== 2}>
        <MapDisplay flight={response.value.flight} />
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
          <button onClick={() => onClose()}>{"Done"}</button>
        )}
      </div>
    </div>
  );
};

export default FlightDisplay;
