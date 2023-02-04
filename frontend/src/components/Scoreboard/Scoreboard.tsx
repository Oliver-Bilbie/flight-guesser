import React, { useState, useEffect } from "react";
import { Box, Text, Heading, Button, Spinner, DataTable } from "grommet";
import { callApi } from "../../helpers/callApi";
import { LOBBY_ENDPOINT } from "../../config";
import { PlayerData, AlertType } from "../../types";
import { Refresh } from "grommet-icons";

interface LobbyMenuProps {
  lobbyId: string;
  lobbyData: PlayerData[];
  refresh: boolean;
  dataSaver: boolean;
  setLobbyData: (data: PlayerData[]) => void;
  setAlert: (alert: AlertType) => void;
}

const LobbyMenu: React.FC<LobbyMenuProps> = ({
  lobbyId,
  lobbyData,
  refresh,
  dataSaver,
  setLobbyData,
  setAlert,
}): React.ReactElement => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initially load the scores of players in the lobby
    // Loads again whenever the value of refresh is flipped
    callGetLobbyData();
    setLoading(false);
  }, [refresh]);

  useEffect(() => {
    // If data-saver is disabled, scores will reload automatically
    // every thirty seconds
    const interval = setInterval(() => {
      if (!dataSaver) {
        callGetLobbyData();
      }
    }, 30000);

    return (): void => clearInterval(interval);
  }, []);

  const callGetLobbyData = (): void => {
    callApi(
      `${LOBBY_ENDPOINT}?lobby_id=${lobbyId}`,
      "GET",
      "",
      handleGetLobbyData
    );
  };

  const handleGetLobbyData = (response): void => {
    // Handles the output from the Get Lobby Data API
    if (response.message) {
      setAlert({ message: response.message, show: true });
    } else {
      // Parse the lobby data string from the API into a JSON array
      const newLobbyData = JSON.parse(
        response.body.replace(/'/g, '"').replace(/}/g, "},").replace(/,]/g, "]")
      );
      setLobbyData(newLobbyData);
    }
  };

  return (
    <Box align="center" direction="column" margin={{ top: "large" }}>
      <Box direction="row" align="center" height="40px">
        <Heading level="2">Leaderboard</Heading>
        {loading ? (
          <Spinner />
        ) : (
          <Button icon={<Refresh />} onClick={callGetLobbyData} />
        )}
      </Box>
      <Heading level="4">Code: {lobbyId}</Heading>
      <DataTable
        data={lobbyData}
        columns={[
          {
            property: "name",
            header: <Text>Name</Text>,
            primary: true,
          },
          { property: "score", header: <Text>Score</Text> },
        ]}
        sort={{ direction: "desc", property: "score" }}
      />
    </Box>
  );
};

export default LobbyMenu;
