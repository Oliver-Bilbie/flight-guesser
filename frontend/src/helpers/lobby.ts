import { LOBBY_ENDPOINT } from "../config";

export const createLobby = (
  name: string,
  score: string,
  onLoad: (response) => void
): void => {
  const request = new XMLHttpRequest();
  const body = `{"name": "${name}", "score": "${score}"}`;

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
        response = { body: request.response.response };
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
    onLoad(response);
  });

  request.open("PUT", LOBBY_ENDPOINT);
  request.send(body);
};

export const joinLobby = (
  name: string,
  score: string,
  lobby_id: string,
  onLoad: (response) => void
): void => {
  const request = new XMLHttpRequest();
  const body = `{"name": "${name}", "score": "${score}", "lobby_id": "${lobby_id}"}`;

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
    onLoad(response);
  });

  request.open("POST", LOBBY_ENDPOINT);
  request.send(body);
};

export const getScores = (
  lobby_id: string,
  onLoad: (response) => void
): void => {
  const request = new XMLHttpRequest();
  const body = `{"lobby_id": "${lobby_id}"}`;

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
    onLoad(response);
  });

  request.open("GET", LOBBY_ENDPOINT);
  request.send(body);
};
