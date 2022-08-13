import React from "react";
import renderer from "react-test-renderer";
import "@testing-library/jest-dom";
import { render, screen, cleanup } from "@testing-library/react";
import Banner from "./Banner";

afterEach(cleanup);

test("Matches snapshot", () => {
  const tree = renderer.create(<Banner />).toJSON();
  expect(tree).toMatchSnapshot();
});

test("Test that the expected elements appear", async () => {
  render(<Banner />);
  expect(screen.getByText("Flight Guesser")).toBeInTheDocument();
  expect(screen.getByLabelText("email")).toBeInTheDocument();
  expect(screen.getByLabelText("github")).toBeInTheDocument();
  expect(screen.getByLabelText("linkedin")).toBeInTheDocument();
});
