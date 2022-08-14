import React, { useState, useEffect } from "react";
import { Box, Button, Heading, Layer, Spinner, Text } from "grommet";
import { Location, Performance } from "grommet-icons";
import AirportSelect from "../AirportSelect/AirportSelect";
import SettingsMenu from "../SettingsMenu/SettingsMenu";
import { handleTurnApi, handleResult } from "../../helpers/handle_turn";
import { getAirportsApi } from "../../helpers/get_airports";

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
    getAirportsApi(setAirports);
    setLoading(false);
  }, []);

  const handleSubmit = (): void => {
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
            handleTurn
          )
        );
      } else {
        setResponse("Please select an airport");
        setShowResponse(true);
      }
    } else {
      setResponse("Location services must be enabled to use this application");
      setShowResponse(true);
    }
  };

  const handleTurn = (response): void => {
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
    <>
      <Box
        direction="column"
        align="center"
        width="large"
        background="light-2"
        elevation="small"
        margin="small"
        round
      >
        {loading ? (
          <Spinner size="large" />
        ) : (
          <Box gap="medium">
            <Heading textAlign="center">Score: {score}</Heading>
            <AirportSelect
              airports={airports}
              setSelection={(selection: string): void =>
                setGuess({ ...guess, origin: selection })
              }
            />
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
        <Layer
          onEsc={(): void => setShowResponse(false)}
          onClickOutside={(): void => setShowResponse(false)}
        >
          <Box
            width="medium"
            pad="small"
            gap="medium"
            align="center"
            justify="center"
          >
            <Text>{response}</Text>
            <Box width="xsmall">
              <Button
                label="Close"
                onClick={(): void => setShowResponse(false)}
              />
            </Box>
          </Box>
        </Layer>
      )}
      {showSettings && (
        <SettingsMenu
          settingsValues={settingsValues}
          setSettingsValues={setSettingsValues}
          onClose={(): void => setShowSettings(false)}
        />
      )}
    </>
  );
};

export default Game;
