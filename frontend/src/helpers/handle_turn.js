export const handleTurnApi = (longitude, latitude, airport, onLoad) => {
  const request = new XMLHttpRequest();
  const body = `{"longitude": ${longitude}, "latitude": ${latitude}, "airport": "${airport}"}`;

  let response = {};

  request.onerror = function () {
    response = { message: "An error has occurred" };
  };
  request.ontimeout = function () {
    response = { message: "The request has timed out" };
  };
  request.onload = function () {
    if (request.status === 200) {
      if (request.response.status === 200) {
        response = { body: request.response.response };
      } else if (request.response.status === 400) {
        response = { message: "No nearby flights were found" };
      } else {
        response = { message: "Data for the nearby flight is not available" };
      }
    } else {
      response = { message: "Unable to fetch data" };
    }
  };

  request.timeout = 30000;
  request.responseType = "json";
  request.addEventListener("load", () => {
    onLoad(response);
  });
  // eslint-disable-next-line no-undef
  request.open("POST", process.env.REACT_APP_ENDPOINT);
  request.send(body);
};

export const handleResult = (response, score, ids) => {
  // search for ids which have already been guessed for to prevent duplication
  const duplicate = ids.find((id) => id === response.id);

  return {
    score: duplicate ? score : score + parseInt(response.score),
    ids: duplicate ? ids : ids.concat(response.id),
    message: `You are looking at ${
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
            }.`,
  };
};
