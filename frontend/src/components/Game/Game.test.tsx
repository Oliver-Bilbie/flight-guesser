import React from "react";
import renderer from "react-test-renderer";
import "@testing-library/jest-dom";
import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import Game from "./Game";
import { ResultType } from "../../types";

// Mock API calls
jest.mock("../../helpers/get_airports", () => ({
  getAirportsApi(): string[] {
    return ["airport 1", "airport 2", "airport 3"];
  },
}));

jest.mock("../../helpers/handle_turn", () => ({
  handleTurnApi(): void {},
  handleResult(): ResultType {
    return {
      message: "test message",
      score: 10,
      ids: ["id1", "id2", "id3"],
    };
  },
}));

// Mock GeoLocation
const mockGeolocation = {
  getCurrentPosition: jest.fn(),
  watchPosition: jest.fn(),
};
// @ts-ignore
global.navigator.geolocation = mockGeolocation;

afterEach(cleanup);

test("Test with no guess", () => {
  render(<Game />);

  // Check that the expected components are rendered
  expect(screen.getByText("Score: 0")).toBeInTheDocument();
  expect(screen.getByText("Make Guess")).toBeInTheDocument();

  // Click on the "Make Guess" button and check that the expected components render
  fireEvent.click(screen.getByText("Make Guess"));
  expect(
    screen.getByText("Please select a destination airport")
  ).toBeInTheDocument();
  expect(screen.getByText("Close")).toBeInTheDocument();
});

// TODO: Write tests where an airport is selected
