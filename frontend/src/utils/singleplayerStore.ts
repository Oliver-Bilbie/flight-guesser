import { create } from "zustand";
import { Rules } from "./types";

type SingleplayerStore = {
  score: number;
  guessedFlights: string[];
  rules: Rules;
  handleGuessResult: (points: number, flightId: string) => void;
  setRules: (rules: Rules) => void;
};

export const useSingleplayerStore = create<SingleplayerStore>((set) => ({
  score: 0,
  guessedFlights: [],
  rules: { useOrigin: false, useDestination: true },

  handleGuessResult: (points, flightId) =>
    set((state) => ({
      score: state.score + points,
      guessedFlights: [...state.guessedFlights, flightId],
    })),

  setRules: (rules) => set({ rules }),
}));
