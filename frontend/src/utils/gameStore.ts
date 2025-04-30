import { create } from "zustand";
import { Rules } from "./types";

type GameStore = {
  score: number;
  guessedFlights: string[];
  rules: Rules;
  handleGuessResult: (points: number, flightId: string) => void;
  setRules: (rules: Rules) => void;
};

export const useGameStore = create<GameStore>((set) => ({
  score: 0,
  guessedFlights: [],
  rules: { useOrigin: true, useDestination: true },

  handleGuessResult: (points, flightId) =>
    set((state) => ({
      score: state.score + points,
      guessedFlights: [...state.guessedFlights, flightId],
    })),

  setRules: (rules) => set({ rules }),
}));
