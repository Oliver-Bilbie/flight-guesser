export const getAirportsApi = (onLoad) => {
  const request = new XMLHttpRequest();

  let response = {};

  request.onerror = function () {
    response = ["An error has occurred"];
  };
  request.ontimeout = function () {
    response = ["The request has timed out"];
  };
  request.onload = function () {
    if (request.status === 200) {
      if (request.response.status === 200) {
        response = request.response.response;
      } else {
        response = ["Failed to load"];
      }
    } else {
      response = ["Failed to load"];
    }
  };

  request.timeout = 10000;
  request.responseType = "json";
  request.addEventListener("load", () => {
    onLoad(response);
  });
  // eslint-disable-next-line no-undef
  request.open("GET", process.env.REACT_APP_ENDPOINT);
  request.send();
};
