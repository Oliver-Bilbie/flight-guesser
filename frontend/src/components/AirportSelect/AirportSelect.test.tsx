import React from "react";
import renderer from "react-test-renderer";
import "@testing-library/jest-dom";
import { render, screen, cleanup, fireEvent } from "@testing-library/react";
import AirportSelect from "./AirportSelect";

const test_airports = ["airport 1", "airport 2", "airport 3"];
const doNothing = (): void => void afterEach(cleanup);

test("Matches snapshot", () => {
  const tree = renderer
    .create(<AirportSelect airports={[]} setSelection={doNothing} />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});

test("Test for no airports", async () => {
  render(<AirportSelect airports={[]} setSelection={doNothing} />);

  // Check that the expected components are rendered
  expect(screen.queryByText("Destination:")).toBeInTheDocument();
  expect(screen.getByLabelText("loading")).toBeInTheDocument();
});

test("Test for error message", async () => {
  render(
    <AirportSelect airports={["Error Message"]} setSelection={doNothing} />
  );

  // Check that the expected components are rendered
  expect(screen.queryByText("Destination:")).toBeInTheDocument();
  expect(screen.queryByText("Error Message")).toBeInTheDocument();
});

test("Test for provided data", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function

  render(<AirportSelect airports={test_airports} setSelection={doNothing} />);

  // Check that the expected components are rendered
  expect(screen.queryByText("Destination:")).toBeInTheDocument();
  expect(screen.queryByPlaceholderText("Select")).toBeInTheDocument();
});

test("Test data selection", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function
  const mockSelection = jest.fn();

  render(
    <AirportSelect airports={test_airports} setSelection={mockSelection} />
  );

  // Test that the provided elements are available for selection
  fireEvent.click(screen.getByPlaceholderText("Select"));
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();

  // Test element selection
  fireEvent.click(screen.getByText("airport 1"));
  fireEvent.click(screen.getByPlaceholderText("Select"));
  fireEvent.click(screen.getByText("airport 2"));
  fireEvent.click(screen.getByPlaceholderText("Select"));
  fireEvent.click(screen.getByText("airport 3"));
  expect(mockSelection).toHaveBeenNthCalledWith(1, "airport 1");
  expect(mockSelection).toHaveBeenNthCalledWith(2, "airport 2");
  expect(mockSelection).toHaveBeenNthCalledWith(3, "airport 3");
});

test("Test data search for '1'", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function

  render(<AirportSelect airports={test_airports} setSelection={doNothing} />);

  // Test that the provided elements are available for selection
  fireEvent.click(screen.getByPlaceholderText("Select"));
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();

  // Test search for "1"
  fireEvent.change(screen.getByPlaceholderText("Search..."), {
    target: { value: "1" },
  });
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).not.toBeInTheDocument();
  expect(screen.queryByText("airport 3")).not.toBeInTheDocument();
});

test("Test data search for '2'", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function

  render(<AirportSelect airports={test_airports} setSelection={doNothing} />);

  // Test that the provided elements are available for selection
  fireEvent.click(screen.getByPlaceholderText("Select"));
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();

  // Test search for "2"
  fireEvent.change(screen.getByPlaceholderText("Search..."), {
    target: { value: "2" },
  });
  expect(screen.queryByText("airport 1")).not.toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).not.toBeInTheDocument();
});

test("Test data search for 'airport'", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function

  render(<AirportSelect airports={test_airports} setSelection={doNothing} />);

  // Test that the provided elements are available for selection
  fireEvent.click(screen.getByPlaceholderText("Select"));
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();

  // Test search for "airport"
  fireEvent.change(screen.getByPlaceholderText("Search..."), {
    target: { value: "airport" },
  });
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();
});

test("Test data search for 'asdf'", async () => {
  window.scrollTo = jest.fn(); // prevents jest error for unsupported function

  render(<AirportSelect airports={test_airports} setSelection={doNothing} />);

  // Test that the provided elements are available for selection
  fireEvent.click(screen.getByPlaceholderText("Select"));
  expect(screen.queryByText("airport 1")).toBeInTheDocument();
  expect(screen.queryByText("airport 2")).toBeInTheDocument();
  expect(screen.queryByText("airport 3")).toBeInTheDocument();

  // Test search for "asdf"
  fireEvent.change(screen.getByPlaceholderText("Search..."), {
    target: { value: "asdf" },
  });
  expect(screen.queryByText("airport 1")).not.toBeInTheDocument();
  expect(screen.queryByText("airport 2")).not.toBeInTheDocument();
  expect(screen.queryByText("airport 3")).not.toBeInTheDocument();
});
