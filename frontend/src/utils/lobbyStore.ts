import { create } from "zustand";
// import { persist } from "zustand/middleware";
import { generateName } from "./generateName";
import { validateGuess } from "./validateGuess";
import {
  Airport,
  defaultRules,
  ErrorStatus,
  FlightMessageResponse,
  GuessResponse,
  LobbyApiResponse,
  Message,
  Rules,
} from "./types";
import { MULTIPLAYER_ENDPOINT } from "./endpoints";

type LobbyStore = {
  isActive: boolean;
  ws: WebSocket | null;

  lobbyId: string | null;
  name: string;
  score: number;
  rules: Rules | null;

  response: GuessResponse;

  setName: (name: string) => void;

  onJoinLobby: (response: LobbyApiResponse) => void;
  onLeaveLobby: () => void;

  clearResponse: () => void;
  setError: (status: ErrorStatus, message: Message) => void;
  makeGuess: (origin?: Airport, destination?: Airport) => void;
  makeApiRequest: (
    location: GeolocationPosition,
    origin?: Airport,
    destination?: Airport,
  ) => void;
  handleGuessResult: (response: FlightMessageResponse) => void;

  initLobby: (lobbyId: string, rules: Rules) => void;
};

export const useLobbyStore = create<LobbyStore>()(
  // persist(
  (set, get) => ({
    isActive: false,
    ws: null,
    lobbyId: null,
    name: generateName(),
    score: 0,
    rules: defaultRules,
    response: { status: "Ready", value: null, error: null },

    setName: (name) => set({ name: name }),

    onJoinLobby: (response) =>
      set(() => {
        return {
          isActive: true,
          lobbyId: response.lobby,
          score: response.score,
          rules: {
            useOrigin: response.rules.use_origin,
            useDestination: response.rules.use_destination,
          },
        };
      }),

    onLeaveLobby: () =>
      set((state) => {
        if (state.ws !== null) {
          state.ws.close();
        }
        return {
          isActive: false,
          ws: null,
          lobbyId: null,
          name: generateName(),
          score: 0,
          rules: null,
        };
      }),

    clearResponse: () =>
      set({ response: { status: "Ready", value: null, error: null } }),

    setError: (status, message) =>
      set({
        response: {
          status: status,
          value: null,
          error: message,
        },
      }),

    makeGuess: (origin, destination) => {
      const { rules, makeApiRequest, setError } = get();
      if (rules === null) {
        setError("ClientError", {
          title: "Client Error",
          message:
            "The game state is invalid. This is a bug, sorry about that!",
        });
        return;
      }
      const validationResult = validateGuess(rules, origin, destination);
      if (validationResult !== null) {
        setError("ClientError", validationResult);
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (location) => makeApiRequest(location, origin, destination),
        (error) =>
          setError("LocationError", {
            title: "Unable to read your location",
            message: error.message,
          }),
        {
          enableHighAccuracy: true,
          timeout: 60000,
          maximumAge: 60000,
        },
      );
    },

    makeApiRequest: (location, origin, destination) => {
      const { lobbyId, name, rules, ws, initLobby, setError } = get();
      const guessMessage = {
        action: "handle_guess",
        lobby_id: lobbyId,
        player_name: name,
        player: {
          lon: location.coords.longitude,
          lat: location.coords.latitude,
        },
        origin: origin?.position,
        destination: destination?.position,
      };

      if (ws === null) {
        // Attempt to reconnect
        if (lobbyId !== null && rules !== null) {
          initLobby(lobbyId, rules);
        }
        if (ws === null) {
          setError("ClientError", {
            title: "Not connected to a server",
            message:
              "The game state is invalid. This is a bug, sorry about that!",
          });
          return;
        }
      }

      ws.send(JSON.stringify(guessMessage));
    },

    handleGuessResult: (response) =>
      set(() => {
        // Don't process blocked flights
        const flightBlocked = response.flight.id === "Blocked-None-None";
        if (flightBlocked) {
          return {
            response: {
              status: "PointsUnavailable",
              value: response,
              error: null,
            },
          };
        }

        // TODO: Pass this from backend
        // Don't add points if already guessed
        // if (state.checkIfGuessed(response.flight.id)) {
        //   return {
        //     response: {
        //       status: "AlreadyGuessed",
        //       value: response,
        //       error: null,
        //     },
        //   };
        // }

        // const pointsAvailable =
        //   (state.rules.useOrigin && response.flight.origin !== null) ||
        //   (state.rules.useDestination && response.flight.destination !== null);
        // const status = pointsAvailable ? "Success" : "PointsUnavailable";

        const status = "Success";

        return {
          score: response.score,
          response: { status: status, value: response, error: null },
        };
      }),

    initLobby: (lobbyId, rules) => {
      set(() => {
        const { name, onJoinLobby, handleGuessResult, setError } = get();

        const ws = new WebSocket(MULTIPLAYER_ENDPOINT);

        ws.onopen = () => {
          console.log("[✅] Connected");

          setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({ action: "ping" }));
            }
          }, 180000);

          if (lobbyId.length === 0) {
            const createLobbyMessage = {
              action: "create_lobby",
              player_name: name,
              rules: {
                use_origin: rules.useOrigin,
                use_destination: rules.useDestination,
              },
            };
            ws.send(JSON.stringify(createLobbyMessage));
            console.log("[📤] Sent create_lobby");
          } else {
            const joinLobbyMessage = {
              action: "join_lobby",
              player_name: name,
              lobby_id: lobbyId,
            };
            ws.send(JSON.stringify(joinLobbyMessage));
            console.log("[📤] Sent join_lobby");
          }
        };

        ws.onmessage = (event) => {
          console.log("[📩] Received:", event.data);

          try {
            const response = JSON.parse(event.data);

            switch (response.event) {
              case "lobby_joined":
                console.log("[🏠] Lobby created with ID:", response.lobby);
                onJoinLobby(response);
                break;

              case "lobby_update":
                break;

              case "flight_details":
                handleGuessResult(response);
                break;

              case "error":
                setError("ApiError", {
                  title: "Server Error",
                  message:
                    response.message === null
                      ? "The server was unable to process your request"
                      : response.message,
                });
                break;

              default:
                break;
            }
          } catch (err) {
            setError("ClientError", {
              title: "Client Error",
              // TODO: Don't print the error directly
              message: String(err),
            });
          }
        };

        ws.onerror = (err) => {
          setError("ClientError", {
            title: "WebSocket Error",
            // TODO: Don't print the error directly
            message: String(err),
          });
        };

        ws.onclose = () => {
          console.log("[❌] Connection closed");
        };

        return { ws: ws };
      });
    },
  }),
  // {
  //   name: "lobbyState",
  // },
  // ),
);
