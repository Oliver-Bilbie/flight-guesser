import { ResponseType } from "../types";

export const callApi = (
  endpoint: string,
  method: "GET" | "POST" | "PUT",
  body: string,
  onLoad: (response: ResponseType) => void
): void => {
  const request = new XMLHttpRequest();

  let response = {};

  request.onerror = (): void => {
    response = { message: "An error has occurred" };
  };
  request.ontimeout = (): void => {
    response = { message: "The request has timed out" };
  };
  request.onload = (): void => {
    if (request.status === 200) {
      if (request.response.status === 200) {
        response = { body: request.response.response };
      } else if (request.response.status === 400) {
        response = { message: "No nearby flights were found" };
      } else {
        response = {
          message: "Unable to fetch data",
        };
      }
    } else {
      response = { message: "Unable to fetch data" };
    }
  };
  request.timeout = 30000;
  request.responseType = "json";
  request.addEventListener("load", (): void => {
    onLoad(response);
  });
  request.addEventListener("timeout", (): void => {
    onLoad(response);
  });
  request.addEventListener("error", (): void => {
    onLoad(response);
  });
  request.open(method, endpoint);
  request.send(body);
};
