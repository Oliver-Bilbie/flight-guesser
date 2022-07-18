import React, { useState } from "react";
import { Box, Button, Layer, Spinner, Text } from "grommet";

const Game = () => {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");
  const [showResponse, setShowResponse] = useState(false);

  const handleSubmit = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(handleApi);
    } else {
      setResponse("Geolocation is not supported by this browser.");
      setShowResponse(true);
    }
  };

  const handleApi = (location) => {
    setLoading(true);
    let request = new XMLHttpRequest();
    const path = "https://nhqos29571.execute-api.eu-west-1.amazonaws.com";
    const body = `{"x": ${location.coords.longitude}, "y": ${location.coords.latitude}}`;

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
          if (request.response.response.destination) {
            setResponse(
              `You are looking at ${["A", "E", "I", "O", "U"].includes(
                request.response.response.aircraft.substring(0, 1).toUpperCase()
              ) ? "an" : "a"} ${
                request.response.response.aircraft
              } aircraft on its way from ${
                request.response.response.origin
              } to ${request.response.response.destination}`
            );
            setShowResponse(true);
          } else {
            setResponse("No flights were found nearby");
            setShowResponse(true);
          }
        } else {
          setResponse("Flight data is unavailable at this time");
          setShowResponse(true);
        }
      } else {
        setResponse("Flight data is unavailable at this time");
        setShowResponse(true);
      }
      setLoading(false);
    };

    request.timeout = 10000;
    request.responseType = "json";
    request.open("POST", path);
    request.send(body);
  };

  return (
    <Box direction="row" align="center">
      {loading ? (<Spinner />) : (<Button label="Get details" onClick={handleSubmit} />)}
      {showResponse && (
        <Layer
          onEsc={() => setShowResponse(false)}
          onClickOutside={() => setShowResponse(false)}
        >
          <Box width="medium" pad="small" gap="medium" align="center" justify="center">
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
