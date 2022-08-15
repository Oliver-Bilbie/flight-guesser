import React, { useState, useEffect } from "react";
import { Box, Button, Heading, Spinner, Stack } from "grommet";
import { Location, Performance } from "grommet-icons";
import AirportSelect from "../AirportSelect/AirportSelect";
import SettingsMenu from "../SettingsMenu/SettingsMenu";
import { handleTurnApi, handleResult } from "../../helpers/handle_turn";
import { getAirportsApi } from "../../helpers/get_airports";
import PopupMenu from "../PopupMenu/PopupMenu";

const Game: React.FC = (): React.ReactElement => {
  const [settingsValues, setSettingsValues] = useState({
    useOrigin: false,
    useDestination: true,
    dataSaver: true,
  });
  const [showSettings, setShowSettings] = useState(false);
  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState("");
  const [showResponse, setShowResponse] = useState(false);
  const [guess, setGuess] = useState({ origin: "", destination: "" });
  const [score, setScore] = useState(0);
  const [ids, setIds] = useState([] as string[]);
  const [airports, setAirports] = useState([] as string[]);

  useEffect(() => {
    // Load a list of airports from an API
    getAirportsApi(setAirports);
    setLoading(false);
  }, []);

  useEffect(() => {
    // Reset guesses if they are disabled in the settings
    setGuess({
      origin: settingsValues.useOrigin ? guess.origin : "",
      destination: settingsValues.useDestination ? guess.destination : "",
    });
  }, [settingsValues]);

  const handleSubmit = (): void => {
    // Validates user inputs and calls the handleTurnApi helper
    if (navigator.geolocation) {
      if (
        (guess.origin !== "" || !settingsValues.useOrigin) &&
        (guess.destination !== "" || !settingsValues.useDestination)
      ) {
        setLoading(true);
        navigator.geolocation.getCurrentPosition((location) =>
          handleTurnApi(
            location.coords.longitude,
            location.coords.latitude,
            guess.origin,
            guess.destination,
            settingsValues.dataSaver,
            handleTurn
          )
        );
      } else {
        setResponse(
          `Please select ${
            guess.origin === "" && settingsValues.useOrigin
              ? "an origin"
              : "a destination"
          } airport`
        );
        setShowResponse(true);
      }
    } else {
      setResponse("Location services must be enabled to use this application");
      setShowResponse(true);
    }
  };

  const handleTurn = (response): void => {
    // Handles the output from the handleTurnApi helper
    if (response.message) {
      setResponse(response.message);
    } else {
      const result = handleResult(response.body, score, ids);
      setResponse(result.message);
      setScore(result.score);
      setIds(result.ids);
    }
    setLoading(false);
    setShowResponse(true);
    setGuess({ origin: "", destination: "" });
  };

  return (
    <Stack anchor="center" interactiveChild={showSettings ? 1 : 0}>
      <Box
        direction="column"
        align="center"
        background="light-2"
        elevation="small"
        margin="small"
        round
      >
        {loading ? (
          <Spinner size="large" pad="small" />
        ) : (
          <Box gap="medium" margin={{ horizontal: "large" }}>
            <Heading textAlign="center">Score: {score}</Heading>
            {settingsValues.useOrigin && (
              <AirportSelect
                label="Origin:"
                value={guess.origin}
                airports={airports}
                setSelection={(selection: string): void =>
                  setGuess({ ...guess, origin: selection })
                }
              />
            )}
            {settingsValues.useDestination && (
              <AirportSelect
                label="Destination:"
                value={guess.destination}
                airports={airports}
                setSelection={(selection: string): void =>
                  setGuess({
                    ...guess,
                    destination: selection,
                  })
                }
              />
            )}
            <Box width="190px" alignSelf="center" pad={{ vertical: "medium" }}>
              <Button
                label="Make Guess"
                icon={<Location />}
                onClick={handleSubmit}
              />
            </Box>
          </Box>
        )}
        <Button
          icon={<Performance />}
          onClick={(): void => setShowSettings(!showSettings)}
          alignSelf="end"
          hoverIndicator
        />
      </Box>
      {showResponse && (
        <PopupMenu
          message={response}
          onClose={(): void => setShowResponse(false)}
        />
      )}
      {showSettings && (
        <SettingsMenu
          settingsValues={settingsValues}
          setSettingsValues={setSettingsValues}
          onClose={(): void => setShowSettings(false)}
        />
      )}
    </Stack>
  );
};

export default Game;
