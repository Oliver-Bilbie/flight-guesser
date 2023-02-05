import React, { useState, useEffect } from "react";
import { Box, Button, Heading, Text, Spinner, Stack } from "grommet";
import { Close, Location, Performance } from "grommet-icons";

import AirportSelect from "../AirportSelect/AirportSelect";
import Scoreboard from "../Scoreboard/Scoreboard";
import SettingsMenu from "../SettingsMenu/SettingsMenu";
import LobbyMenu from "../LobbyMenu/LobbyMenu";
import PopupMenu from "../PopupMenu/PopupMenu";

import { handleResult } from "../../helpers/handle_turn";
import { callApi } from "../../helpers/callApi";
import { settingsToRules, rulesToSettings } from "../../helpers/gameRules";
import { AIRPORT_ENDPOINT, TURN_ENDPOINT } from "../../config";
import { LobbyMode, PlayerData } from "../../types";

const Game: React.FC = (): React.ReactElement => {
  const [settingsValues, setSettingsValues] = useState({
    useOrigin: false,
    useDestination: true,
    dataSaver: true,
  });
  const [showSettings, setShowSettings] = useState(false);
  const [showLobbyMenu, setShowLobbyMenu] = useState(LobbyMode.hidden);
  const [loading, setLoading] = useState(true);
  const [alert, setAlert] = useState({ message: "", show: false });
  const [guess, setGuess] = useState({ origin: "", destination: "" });
  const [score, setScore] = useState(0);
  const [ids, setIds] = useState([] as string[]);
  const [airports, setAirports] = useState([] as string[]);
  const [playerId, setPlayerId] = useState("");
  const [lobbyId, setLobbyId] = useState("");
  const [lobbyData, setLobbyData] = useState([] as PlayerData[]);
  const [lockSettings, setLockSettings] = useState(false);
  const [refreshScores, setRefreshScores] = useState(false);

  useEffect(() => {
    // Load a list of airports from an API
    callApi(AIRPORT_ENDPOINT, "GET", "", handleAirports);
    setLoading(false);
  }, []);

  useEffect(() => {
    // Reset guesses if they are disabled in the settings
    setGuess({
      origin: settingsValues.useOrigin ? guess.origin : "",
      destination: settingsValues.useDestination ? guess.destination : "",
    });
  }, [settingsValues]);

  const handleAirports = (response): void => {
    // Handles the output from the airport API
    if (response.message) {
      setAlert({ message: response.message, show: true });
    } else {
      setAirports(response.body);
    }
  };

  const handleSubmit = (): void => {
    // Validates user inputs and calls the handleTurnApi helper
    if (navigator.geolocation) {
      if (
        (guess.origin !== "" || !settingsValues.useOrigin) &&
        (guess.destination !== "" || !settingsValues.useDestination)
      ) {
        navigator.geolocation.getCurrentPosition(
          (location) => {
            setLoading(true);
            const body =
              `{` +
              `"longitude": ${location.coords.longitude},` +
              `"latitude": ${location.coords.latitude},` +
              `"origin": "${guess.origin}",` +
              `"destination": "${guess.destination}",` +
              `"player_id": "${playerId}"` +
              `}`;
            callApi(TURN_ENDPOINT, "POST", body, handleTurn);
          },
          (): void => {
            setAlert({
              message:
                "Location services must be enabled to use this application",
              show: true,
            });
          }
        );
      } else {
        setAlert({
          message: `Please select ${
            guess.origin === "" && settingsValues.useOrigin
              ? "an origin"
              : "a destination"
          } airport`,
          show: true,
        });
      }
    } else {
      setAlert({
        message: "Location services are not supported by your browser",
        show: true,
      });
    }
  };

  const handleTurn = (response): void => {
    // Handles the output from the turn API
    if (response.message) {
      setAlert({ message: response.message, show: true });
    } else {
      const result = handleResult(response.body, score, ids);
      setAlert({ message: result.message, show: true });
      setScore(result.score);
      setIds(result.ids);
    }
    setLoading(false);
    setRefreshScores(!refreshScores);
    setGuess({ origin: "", destination: "" });
  };

  const handleJoinLobby = (response): void => {
    // Handles the output from the Join Lobby API
    if (response.message) {
      setAlert({ message: response.message, show: true });
      setLockSettings(false);
      setPlayerId("");
    } else {
      setPlayerId(response.body.player_id);

      // Parse the lobby data string from the API into a JSON array
      const newLobbyData = JSON.parse(
        response.body.lobby_data
          .replace(/'/g, '"')
          .replace(/}/g, "},")
          .replace(/,]/g, "]")
      );
      setLobbyData(newLobbyData);

      // Retrieve the player's previous score from the lobby data
      newLobbyData.map((playerData: PlayerData): void => {
        if (playerData.player_id === response.body.player_id) {
          setScore(playerData.score);
        }
      });

      // Configure settings to match the lobby's rules
      const newSettings = rulesToSettings(response.body.rules);
      setSettingsValues({
        useOrigin: newSettings.useOrigin,
        useDestination: newSettings.useDestination,
        dataSaver: settingsValues.dataSaver,
      });
    }
  };

  const handleCreateLobby = (response): void => {
    // Handles the output from the Create Lobby API
    if (response.message) {
      setAlert({ message: response.message, show: true });
      setLockSettings(false);
      setPlayerId("");
    } else {
      setLobbyId(response.body.lobby_id);
      setPlayerId(response.body.player_id);

      // Parse the lobby data string from the API into a JSON array
      const newLobbyData = JSON.parse(
        response.body.lobby_data
          .replace(/'/g, '"')
          .replace(/}/g, "},")
          .replace(/,]/g, "]")
      );
      setLobbyData(newLobbyData);
    }
  };

  return (
    <Stack anchor="center">
      {showSettings ? (
        <SettingsMenu
          settingsValues={settingsValues}
          locked={lockSettings}
          setSettingsValues={setSettingsValues}
          setShowLobbyMenu={setShowLobbyMenu}
          onClose={(): void => setShowSettings(false)}
        />
      ) : (
        <Box
          direction="column"
          align="center"
          background="light-2"
          elevation="small"
          margin="small"
          round
        >
          {loading ? (
            <Box
              width="300px"
              height="361px"
              align="center"
              justify="center"
              gap="medium"
              margin={{ horizontal: "large" }}
            >
              <Spinner size="large" pad="small" />
            </Box>
          ) : (
            <Box gap="medium" align="center" margin={{ horizontal: "large" }}>
              <Box width="300px" />
              {lobbyId === "" && (
                <Heading textAlign="center">Score: {score}</Heading>
              )}
              {settingsValues.useOrigin && (
                <AirportSelect
                  label="Origin:"
                  value={guess.origin}
                  airports={airports}
                  setSelection={(selection: string): void =>
                    setGuess({
                      ...guess,
                      origin: selection,
                    })
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
              <Box
                width="190px"
                alignSelf="center"
                pad={{ vertical: "medium" }}
              >
                <Button
                  label="Make Guess"
                  icon={<Location />}
                  onClick={handleSubmit}
                />
              </Box>
            </Box>
          )}
          {lobbyId !== "" && (
            <Scoreboard
              lobbyId={lobbyId}
              lobbyData={lobbyData}
              refresh={refreshScores}
              dataSaver={settingsValues.dataSaver}
              setLobbyData={setLobbyData}
              setAlert={setAlert}
            />
          )}
          <Button
            icon={<Performance />}
            onClick={(): void => setShowSettings(!showSettings)}
            alignSelf="end"
            hoverIndicator
          />
        </Box>
      )}
      {alert.show && (
        <PopupMenu
          body={<Text>{alert.message}</Text>}
          buttons={[
            {
              label: "Close",
              icon: <Close />,
              onClick: (): void => setAlert({ ...alert, show: false }),
            },
          ]}
        />
      )}
      {showLobbyMenu !== LobbyMode.hidden && (
        <LobbyMenu
          mode={showLobbyMenu}
          score={score}
          rules={settingsToRules(
            settingsValues.useOrigin,
            settingsValues.useDestination
          )}
          guessedFlights={ids}
          setLobbyId={setLobbyId}
          onJoinLobby={handleJoinLobby}
          onCreateLobby={handleCreateLobby}
          lockSettings={(): void => setLockSettings(true)}
          onClose={(): void => {
            setShowSettings(false);
            setShowLobbyMenu(LobbyMode.hidden);
          }}
        />
      )}
    </Stack>
  );
};

export default Game;
