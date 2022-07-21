import React, { useState, useEffect } from "react";
import { Box, Button, Heading, Layer, Spinner, Text } from "grommet";
import { Location } from "grommet-icons";
import AirportSelect from "./AirportSelect";
import { handleTurnApi, handleResult } from "../helpers/handle_turn";
import { getAirportsApi } from "../helpers/get_airports";

const Game = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [showResponse, setShowResponse] = useState(false);
  const [airport, setAirport] = useState("");
  const [score, setScore] = useState(0);
  const [ids, setIds] = useState([]);
  const [airports, setAirports] = useState([]);

  useEffect(() => {
    getAirportsApi(setAirports);
  }, []);

  const handleSubmit = () => {
    if (navigator.geolocation) {
      if (airport !== "") {
        setLoading(true);
        navigator.geolocation.getCurrentPosition((location) =>
          handleTurnApi(
            location.coords.longitude,
            location.coords.latitude,
            airport,
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

  const handleTurn = (response) => {
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
    setAirport("");
  };

  return (
    <Box direction="row" align="center">
      {loading ? (
        <Spinner size="large" />
      ) : (
        <Box gap="medium">
          <Heading textAlign="center">Score: {score}</Heading>
          <AirportSelect airports={airports} setSelection={setAirport} />
          <Box width="190px" alignSelf="center" pad={{ vertical: "medium" }}>
            <Button
              label="Make Guess"
              icon={<Location />}
              onClick={handleSubmit}
            />
          </Box>
        </Box>
      )}
      {showResponse && (
        <Layer
          onEsc={() => setShowResponse(false)}
          onClickOutside={() => setShowResponse(false)}
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
              <Button label="Close" onClick={() => setShowResponse(false)} />
            </Box>
          </Box>
        </Layer>
      )}
    </Box>
  );
};

export default Game;
