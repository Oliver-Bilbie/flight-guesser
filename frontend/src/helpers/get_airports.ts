import { AIRPORT_ENDPOINT } from "../config";

export const getAirportsApi = (onLoad: (airports: string[]) => void): void => {
  const request = new XMLHttpRequest();

  let response = {};

  request.onerror = (): void => {
    response = ["An error has occurred"];
  };
  request.ontimeout = (): void => {
    response = ["The request has timed out"];
  };
  request.onload = (): void => {
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
  request.addEventListener("load", (): void => {
    onLoad(response as string[]);
  });

  request.open("GET", AIRPORT_ENDPOINT);
  request.send();
};
