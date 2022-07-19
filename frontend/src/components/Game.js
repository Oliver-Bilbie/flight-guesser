import React, { useState } from "react";
import { Box, Button, Heading, Layer, Spinner, Text } from "grommet";
import { Location } from "grommet-icons";
import AirportSelect from "./AirportSelect";

const Game = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [showResponse, setShowResponse] = useState(false);
  const [airport, setAirport] = useState("");
  const [score, setScore] = useState(0);
  const [ids, setIds] = useState([]);

  const handleSubmit = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(handleApi);
    } else {
      setResponse("Geolocation is not supported by this browser.");
      setShowResponse(true);
    }
  };

  const handleResult = (response) => {
    // search for ids which have already been guessed for to prevent duplication
    const duplicate = ids.find((id) => id === response.id);
    if (!duplicate) {
      // only award points for first guesses
      setScore(score + parseInt(response.score));
      setIds(ids.concat(response.id));
    }

    setResponse(
      `You are looking at ${
        ["A", "E", "I", "O", "U"].includes(
          response.aircraft.substring(0, 1).toUpperCase()
        )
          ? "an"
          : "a"
      } ${response.aircraft} aircraft on its way from ${response.origin} to ${
        response.destination
      }.
      You have ${
        duplicate
          ? `already made a guess for this flight`
          : `scored ${response.score} points`
      }.`
    );
  };

  const handleApi = (location) => {
    setLoading(true);
    let request = new XMLHttpRequest();
    const path = process.env.REACT_APP_ENDPOINT;
    const body = `{"x": ${location.coords.longitude}, "y": ${location.coords.latitude}, "airport": "${airport}"}`;

    request.onerror = function () {
      setResponse("An error has occurred");
      setLoading(false);
      setShowResponse(true);
    };
    request.ontimeout = function () {
      setResponse("The request has timed out");
      setLoading(false);
      setShowResponse(true);
    };
    request.onload = function () {
      if (request.status === 200) {
        if (request.response.status === 200) {
          handleResult(request.response.response);
        } else if (request.response.status === 400) {
          setResponse("No nearby flights were found");
        } else {
          setResponse("Data for the nearby flight is not available");
        }
      } else {
        setResponse("Unable to fetch data");
      }
      setLoading(false);
      setShowResponse(true);
    };

    request.timeout = 30000;
    request.responseType = "json";
    request.open("POST", path);
    request.send(body);
  };

  return (
    <Box direction="row" align="center">
      {loading ? (
        <Spinner size="large" />
      ) : (
        <Box gap="medium">
          <Heading textAlign="center">Score: {score}</Heading>
          <Text>Destination:</Text>
          <AirportSelect handleSelection={setAirport} />
          <Box width="190px" alignSelf="center" pad={{vertical: "medium"}}>
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
