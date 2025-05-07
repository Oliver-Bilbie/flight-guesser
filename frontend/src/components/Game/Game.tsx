import { ReactElement, useState, FC } from "react";
import "./Game.css";
import AirportProvider from "../AirportProvider/AirportProvider";
import AirportSelector from "../AirportSelector/AirportSelector";
import FlightDisplay from "../FlightDisplay/FlightDisplay";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";
import MessageDisplay from "../MessageDisplay/MessageDisplay";
import { useGameStore } from "../../utils/gameStore";
import { useLobbyStore } from "../../utils/lobbyStore";
import { Airport, isErrorStatus, isSuccessStatus } from "../../utils/types";

const Game: FC = (): ReactElement => {
  const [origin, setOrigin] = useState<Airport>();
  const [destination, setDestination] = useState<Airport>();

  const singleRules = useGameStore((state) => state.rules);
  const singleResponse = useGameStore((state) => state.response);
  const singleMakeGuess = useGameStore((state) => state.makeGuess);
  const singleClearResponse = useGameStore((state) => state.clearResponse);

  const isMultiplayer =
    useLobbyStore((state) => state.lobbyResponse.status) === "Ready";
  const multiRules = useLobbyStore((state) => state.rules);
  const multiResponse = useLobbyStore((state) => state.guessResponse);
  const multiMakeGuess = useLobbyStore((state) => state.makeGuess);
  const multiClearResponse = useLobbyStore((state) => state.clearGuessResponse);

  const rules = isMultiplayer ? multiRules : singleRules;
  const response = isMultiplayer ? multiResponse : singleResponse;
  const makeGuess = isMultiplayer ? multiMakeGuess : singleMakeGuess;
  const clearResponse = isMultiplayer
    ? multiClearResponse
    : singleClearResponse;

  const rulesMissing = rules === null;
  const allDisabled =
    !rulesMissing && !rules.useOrigin && !rules.useDestination;

  function clearAll() {
    setOrigin(undefined);
    setDestination(undefined);
    clearResponse();
  }

  return (
    <AirportProvider>
      {response.status === "Loading" ? (
        <div className="game-loading">
          <LoadingSpinner />
        </div>
      ) : isSuccessStatus(response.status) ? (
        response.value !== null && <FlightDisplay onClose={() => clearAll()} />
      ) : isErrorStatus(response.status) ? (
        <MessageDisplay
          title={response.error?.title ? response.error.title : "Error"}
          message={response.error?.message ? response.error.message : ""}
          continueText={"Back"}
          onContinue={() => clearResponse()}
        />
      ) : (
        // TODO: Replace with hide menu
        rules !== null && (
          <>
            <div className="game">
              {rules.useOrigin && (
                <>
                  <h4 className="game-label">Origin:</h4>
                  <AirportSelector onSelect={(airport) => setOrigin(airport)} />
                </>
              )}

              {rules.useDestination && (
                <>
                  <h4 className="game-label">Destination:</h4>
                  <AirportSelector
                    onSelect={(airport) => setDestination(airport)}
                  />
                </>
              )}

              {allDisabled && (
                <h4 className="game-warning">
                  You have disabled all types of guesses from the settings menu.
                  You will need to re-enable something in order to make a guess.
                </h4>
              )}
            </div>

            {!allDisabled && (
              <button
                className="game-button"
                onClick={() => makeGuess(origin, destination)}
              >
                Make guess
              </button>
            )}
          </>
        )
      )}
    </AirportProvider>
  );
};

export default Game;
