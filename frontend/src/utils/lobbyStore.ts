import { create } from "zustand";
import { persist } from "zustand/middleware";
import { generateName } from "./generateName";
import { validateGuess } from "./validateGuess";
import { useGameStore } from "./gameStore";
import { MULTIPLAYER_ENDPOINT } from "./endpoints";
import {
  Airport,
  defaultRules,
  ErrorStatus,
  FlightMessageResponse,
  GuessResponse,
  LobbyApiResponse,
  LobbyResponse,
  LobbyStatus,
  Message,
  PlayerData,
  Rules,
} from "./types";

type LobbyStore = {
  ws: WebSocket | null;
  lobbyId: string | null;
  name: string;
  score: number;
  rules: Rules | null;
  players: PlayerData[];
  guessResponse: GuessResponse;
  lobbyResponse: LobbyResponse;

  setName: (name: string) => void;

  setGuessLoading: () => void;
  setGuessError: (status: ErrorStatus, message: Message) => void;
  makeGuess: (origin?: Airport, destination?: Airport) => void;
  makeApiRequest: (
    location: GeolocationPosition,
    origin?: Airport,
    destination?: Airport,
    firstTry?: boolean,
  ) => void;
  handleGuessResult: (response: FlightMessageResponse) => void;
  clearGuessResponse: () => void;

  getLobbyStatus: () => LobbyStatus;
  setLobbyLoading: () => void;
  setLobbyError: (message: Message) => void;
  initLobby: (lobbyId: string, rules: Rules) => void;
  onJoinLobby: (response: LobbyApiResponse) => void;
  onUpdateLobby: (response: LobbyApiResponse) => void;
  onLeaveLobby: () => void;
};

export const useLobbyStore = create<LobbyStore>()(
  persist(
    (set, get) => ({
      ws: null,
      lobbyId: null,
      name: generateName(),
      score: 0,
      rules: defaultRules,
      players: [],
      guessResponse: { status: "Ready", value: null, error: null },
      lobbyResponse: { status: "NotInLobby", error: null },

      setName: (name) => set({ name: name }),

      onJoinLobby: (response) =>
        set(() => {
          return {
            lobbyId: response.lobby,
            score: response.score,
            rules: {
              useOrigin: response.rules.use_origin,
              useDestination: response.rules.use_destination,
            },
            players: response.players,
            lobbyResponse: { status: "Ready", error: null },
          };
        }),

      onUpdateLobby: (response) =>
        set(() => {
          return {
            players: response.players,
          };
        }),

      onLeaveLobby: () =>
        set((state) => {
          if (state.ws !== null) {
            state.ws.close();
          }

          // Reset the singleplayer response
          const clearResponse = useGameStore.getState().clearResponse;
          clearResponse();

          return {
            ws: null,
            lobbyId: null,
            name: generateName(),
            score: 0,
            rules: null,
            players: [],
            lobbyResponse: { status: "NotInLobby", error: null },
          };
        }),

      clearGuessResponse: () =>
        set({ guessResponse: { status: "Ready", value: null, error: null } }),

      setGuessLoading: () =>
        set({ guessResponse: { status: "Loading", value: null, error: null } }),

      getLobbyStatus: () => {
        const { lobbyResponse } = get();
        return lobbyResponse.status;
      },

      setLobbyLoading: () =>
        set((state) => {
          setTimeout(() => {
            if (state.getLobbyStatus() === "Loading") {
              state.setLobbyError({
                title: "Unable to connect",
                message: "Connection to lobby timed out",
              });
            }
          }, 10000);

          return {
            lobbyResponse: { status: "Loading", error: null },
          };
        }),

      setLobbyError: (message) =>
        set({ lobbyResponse: { status: "Error", error: message } }),

      setGuessError: (status, message) =>
        set({
          guessResponse: {
            status: status,
            value: null,
            error: message,
          },
        }),

      makeGuess: (origin, destination) => {
        const {
          rules,
          makeApiRequest,
          setGuessLoading: setLoading,
          setGuessError: setError,
        } = get();

        setLoading();

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

      makeApiRequest: (location, origin, destination, firstTry = true) => {
        const {
          lobbyId,
          name,
          rules,
          ws,
          initLobby,
          setGuessError: setError,
          makeApiRequest,
        } = get();

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
          if (firstTry) {
            // Attempt to reconnect
            if (lobbyId !== null && rules !== null) {
              initLobby(lobbyId, rules);
              setTimeout(
                () => makeApiRequest(location, origin, destination, false),
                3000,
              );
            }
          } else {
            setError("ClientError", {
              title: "Disconnected from server",
              message:
                "You have lost connection to the multiplayer server. Please wait a moment and try again.",
            });
          }
          return;
        }

        ws.send(JSON.stringify(guessMessage));
      },

      handleGuessResult: (response) =>
        set(() => {
          // Forward the response to the singleplayer method.
          // This allows the player to retain guesses and points after leaving the lobby.
          const singlePlayerHandler = useGameStore.getState().handleGuessResult;
          singlePlayerHandler(response);

          return {
            score: response.score,
            guessResponse: {
              status: response.status,
              value: response,
              error: null,
            },
          };
        }),

      initLobby: (lobbyId, rules) => {
        set(() => {
          const {
            name,
            ws,
            setLobbyLoading,
            onJoinLobby,
            onUpdateLobby,
            handleGuessResult,
            setGuessError,
            setLobbyError,
          } = get();

          if (ws !== null) {
            ws.close();
          }

          setLobbyLoading();

          const newWs = new WebSocket(MULTIPLAYER_ENDPOINT);

          newWs.onopen = () => {
            console.log("[✅] Connected");

            setInterval(() => {
              if (newWs.readyState === WebSocket.OPEN) {
                newWs.send(JSON.stringify({ action: "ping" }));
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
              newWs.send(JSON.stringify(createLobbyMessage));
              console.log("[📤] Sent create_lobby");
            } else {
              const joinLobbyMessage = {
                action: "join_lobby",
                player_name: name,
                lobby_id: lobbyId,
              };
              newWs.send(JSON.stringify(joinLobbyMessage));
              console.log("[📤] Sent join_lobby");
            }
          };

          newWs.onmessage = (event) => {
            console.log("[📩] Received:", event.data);

            try {
              const response = JSON.parse(event.data);

              switch (response.event) {
                case "lobby_joined":
                  console.log("[🏠] Lobby created with ID:", response.lobby);
                  onJoinLobby(response);
                  break;

                case "lobby_update":
                  onUpdateLobby(response);
                  break;

                case "flight_details":
                  handleGuessResult(response);
                  break;

                case "lobby_error":
                  setLobbyError({
                    title: "Server Error",
                    message:
                      response.message === null
                        ? "The server was unable to process your request"
                        : response.message,
                  });
                  break;

                case "flight_error":
                  setGuessError("ApiError", {
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
              console.log(err);
            }
          };

          newWs.onerror = (err) => {
            setLobbyError({
              title: "WebSocket Error",
              message: String(err),
            });
          };

          newWs.onclose = () => {
            console.log("[❌] Connection closed");
          };

          return { ws: newWs };
        });
      },
    }),
    {
      name: "lobbyState",
      partialize: (state) => {
        const {
          guessResponse: _gresp,
          lobbyResponse: _lresp,
          ws: _ws,
          ...rest
        } = state;
        return rest;
      },
    },
  ),
);
