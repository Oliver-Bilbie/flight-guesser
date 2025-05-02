import { ReactElement, useState, FC } from "react";
import "./MakeGuess.css";
import AirportProvider from "../AirportProvider/AirportProvider";
import AirportSelector from "../AirportSelector/AirportSelector";
import FlightDisplay from "../FlightDisplay/FlightDisplay";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";
import MessageDisplay from "../MessageDisplay/MessageDisplay";
import { useGameStore } from "../../utils/gameStore";
import {
  Rules,
  Airport,
  Flight,
  FlightApiResponse,
  Points,
  ErrorData,
  FlightApiError,
  zeroPoints,
  emptyError,
} from "../../utils/types";
import { SINGLEPLAYER_ENDPOINT } from "../../utils/endpoints";

const MakeGuess: FC = (): ReactElement => {
  const [origin, setOrigin] = useState<Airport>();
  const [destination, setDestination] = useState<Airport>();
  const [isLoading, setIsLoading] = useState(false);
  const [alreadyGuessed, setAlreadyGuessed] = useState(true);
  const [points, setPoints] = useState<Points>(zeroPoints);
  const [flight, setFlight] = useState<Flight>();
  const [error, setError] = useState<ErrorData>(emptyError);

  const rules = useGameStore((state) => state.rules);
  const handleGuessResult = useGameStore((state) => state.handleGuessResult);
  const checkIfGuessed = useGameStore((state) => state.checkIfGuessed);

  const allDisabled = !rules.useOrigin && !rules.useDestination;

  async function makeGuessRequest(
    location: GeolocationPosition,
    rules: Rules,
    origin?: Airport,
    destination?: Airport,
  ) {
    try {
      // TODO: Remove debugging
      // const player = {
      //   lon: 8.541694,
      //   lat: 47.376888,
      // };
      const player = {
        lon: location.coords.longitude,
        lat: location.coords.latitude,
      };
      const response = await fetch(SINGLEPLAYER_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({
          player: player,
          rules: rules,
          origin: origin?.position,
          destination: destination?.position,
        }),
      });

      if (response.ok) {
        const body: FlightApiResponse = await response.json();
        setAlreadyGuessed(checkIfGuessed(body.flight.id));
        setPoints(body.points);
        setFlight(body.flight);
        handleGuessResult(body.points.total, body.flight.id);
      } else {
        const body: FlightApiError = await response.json();
        setError({
          show: true,
          title: "Unable to make guess",
          message: body.message,
          continueText: "Back",
          onContinue: () => setError(emptyError),
        });
      }
    } catch (error) {
      setError({
        show: true,
        title: "Unable to make guess",
        message: "Something went wrong when trying to contact the server",
        continueText: "Back",
        onContinue: () => setError(emptyError),
      });
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  function handlePositionError(
    error: GeolocationPositionError,
    rules: Rules,
    origin?: Airport,
    destination?: Airport,
  ) {
    setError({
      show: true,
      title: "Unable to read your location",
      message: error.message,
      continueText: "Retry",
      onContinue: () => {
        setError(emptyError);
        handleSubmit(rules, origin, destination);
      },
    });
    setIsLoading(false);
  }

  async function handleSubmit(
    rules: Rules,
    origin?: Airport,
    destination?: Airport,
  ) {
    if (validateGuess(rules, origin, destination)) {
      setIsLoading(true);
      navigator.geolocation.getCurrentPosition(
        (location) => makeGuessRequest(location, rules, origin, destination),
        (error) => handlePositionError(error, rules, origin, destination),
        {
          enableHighAccuracy: true,
          timeout: 60000,
          maximumAge: 60000,
        },
      );
    }
  }

  function validateGuess(
    rules: Rules,
    origin?: Airport,
    destination?: Airport,
  ) {
    const originMissing = rules.useOrigin && origin == null;
    const destinationMissing = rules.useDestination && destination == null;
    const bothMissing = originMissing && destinationMissing;
    const isInvalid = originMissing || destinationMissing;

    if (isInvalid) {
      // This message should never be shown, but is provided as a failsafe
      let title = "Invalid guess";
      let message = "Please review your inputs are try again.";

      if (bothMissing) {
        title = "Neither of the airports were provided";
        message =
          "To make a guess, provide guesses for the origin and destination airports.";
      } else if (originMissing) {
        title = "An origin airport was not provided";
        message =
          "To make a guess, either provide an origin airport or disable origin guesses from the settings menu.";
      } else if (destinationMissing) {
        title = "A destination airport was not provided";
        message =
          "To make a guess, either provide an destination airport or disable origin guesses from the settings menu.";
      }

      setError({
        show: true,
        title: title,
        message: message,
        continueText: "Back",
        onContinue: () => setError(emptyError),
      });

      return false;
    }
    return true;
  }

  function clearGuess() {
    setOrigin(undefined);
    setDestination(undefined);
    setPoints(zeroPoints);
    setFlight(undefined);
    setIsLoading(false);
  }

  return (
    <AirportProvider>
      {isLoading ? (
        <div className="make-guess-loading">
          <LoadingSpinner />
        </div>
      ) : error.show ? (
        <MessageDisplay
          title={error.title}
          message={error.message}
          continueText={error.continueText}
          onContinue={error.onContinue}
        />
      ) : (
        <>
          {flight ? (
            <FlightDisplay
              flight={flight}
              points={points}
              alreadyGuessed={alreadyGuessed}
              onClose={() => clearGuess()}
            />
          ) : (
            <>
              <div className="make-guess">
                {rules.useOrigin && (
                  <>
                    <h4 className="make-guess-label">Origin:</h4>
                    <AirportSelector
                      onSelect={(airport) => setOrigin(airport)}
                    />
                  </>
                )}

                {rules.useDestination && (
                  <>
                    <h4 className="make-guess-label">Destination:</h4>
                    <AirportSelector
                      onSelect={(airport) => setDestination(airport)}
                    />
                  </>
                )}

                {allDisabled && (
                  <h4 className="make-guess-warning">
                    You have disabled all types of guesses from the settings
                    menu. You will need to re-enable something in order to make
                    a guess.
                  </h4>
                )}
              </div>

              {!allDisabled && (
                <button
                  className="make-guess-button"
                  onClick={() => handleSubmit(rules, origin, destination)}
                >
                  Make guess
                </button>
              )}
            </>
          )}
        </>
      )}
    </AirportProvider>
  );
};

export default MakeGuess;
