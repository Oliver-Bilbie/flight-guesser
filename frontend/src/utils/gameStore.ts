import { create } from "zustand";
import { persist } from "zustand/middleware";
import { Rules } from "./types";

type GameStore = {
  score: number;
  guessedFlights: string[];
  rules: Rules;
  checkIfGuessed: (flightId: string) => boolean;
  handleGuessResult: (points: number, flightId: string) => void;
  setRules: (rules: Rules) => void;
};

export const useGameStore = create<GameStore>()(
  persist(
    (set, get) => ({
      score: 0,
      guessedFlights: [],
      rules: { useOrigin: true, useDestination: true },

      checkIfGuessed: (flightId) => {
        const { guessedFlights } = get();
        return guessedFlights.includes(flightId);
      },

      handleGuessResult: (points, flightId) =>
        set((state) => {
          // Don't process blocked flights
          if (flightId === "Blocked-None-None") {
            return state;
          }

          // Don't add points if already guessed
          const { checkIfGuessed: alreadyGuessed } = get();
          if (alreadyGuessed(flightId)) {
            return state;
          }

          return {
            score: state.score + points,
            guessedFlights: [...state.guessedFlights, flightId],
          };
        }),

      setRules: (rules) => set({ rules }),
    }),
    {
      name: "gameState",
    },
  ),
);
