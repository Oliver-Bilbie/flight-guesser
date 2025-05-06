import { create } from "zustand";
// import { persist } from "zustand/middleware";
import { validateGuess } from "./validateGuess";
import { SINGLEPLAYER_ENDPOINT } from "./endpoints";
import {
  Airport,
  defaultRules,
  ErrorStatus,
  FlightApiError,
  FlightApiResponse,
  GuessResponse,
  Message,
  Rules,
  SuccessStatus,
} from "./types";

type GameStore = {
  score: number;
  guessedFlights: string[];
  rules: Rules;

  response: GuessResponse;

  checkIfGuessed: (flightId: string) => boolean;
  setRules: (rules: Rules) => void;
  clearResponse: () => void;
  reset: () => void;

  setFlight: (status: SuccessStatus, response: FlightApiResponse) => void;
  setLoading: () => void;
  setError: (status: ErrorStatus, message: Message) => void;

  makeGuess: (origin?: Airport, destination?: Airport) => void;
  makeApiRequest: (
    location: GeolocationPosition,
    origin?: Airport,
    destination?: Airport,
  ) => void;
  handleGuessResult: (response: FlightApiResponse) => void;
};

export const useGameStore = create<GameStore>()(
  // persist(
  (set, get) => ({
    score: 0,
    guessedFlights: [],
    rules: defaultRules,
    response: { status: "Ready", value: null, error: null },

    checkIfGuessed: (flightId) => {
      const { guessedFlights } = get();
      return guessedFlights.includes(flightId);
    },

    setRules: (rules) => set({ rules }),

    clearResponse: () =>
      set({ response: { status: "Ready", value: null, error: null } }),

    reset: () => set({ score: 0, guessedFlights: [] }),

    setFlight: (status, response) =>
      set({
        response: {
          status: status,
          value: response,
          error: null,
        },
      }),

    setLoading: () =>
      set({ response: { status: "Loading", value: null, error: null } }),

    setError: (status, message) =>
      set({
        response: {
          status: status,
          value: null,
          error: message,
        },
      }),

    makeGuess: (origin, destination) => {
      const { rules, makeApiRequest, setLoading, setError } = get();

      setLoading();

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

    makeApiRequest: async (location, origin, destination) => {
      const { rules, handleGuessResult, setError } = get();

      try {
        const response = await fetch(SINGLEPLAYER_ENDPOINT, {
          method: "POST",
          body: JSON.stringify({
            player: {
              lon: location.coords.longitude,
              lat: location.coords.latitude,
            },
            rules: rules,
            origin: origin?.position,
            destination: destination?.position,
          }),
        });

        if (response.ok) {
          const body: FlightApiResponse = await response.json();
          handleGuessResult(body);
          return;
        } else {
          const body: FlightApiError = await response.json();
          setError("ApiError", {
            title: "Unable to make guess",
            message: body.message,
          });
          return;
        }
      } catch (error) {
        setError("ApiError", {
          title: "Unable to make guess",
          message: "Something went wrong when trying to contact the server",
        });
        console.error(error);
        return;
      }
    },

    handleGuessResult: (response) =>
      set((state) => {
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

        // Don't add points if already guessed
        if (state.checkIfGuessed(response.flight.id)) {
          return {
            response: {
              status: "AlreadyGuessed",
              value: response,
              error: null,
            },
          };
        }

        const pointsAvailable =
          (state.rules.useOrigin && response.flight.origin !== null) ||
          (state.rules.useDestination && response.flight.destination !== null);
        const status = pointsAvailable ? "Success" : "PointsUnavailable";

        return {
          score: state.score + response.points.total,
          guessedFlights: [...state.guessedFlights, response.flight.id],
          response: { status: status, value: response, error: null },
        };
      }),
  }),
  // {
  //   name: "gameState",
  // },
  // ),
);
