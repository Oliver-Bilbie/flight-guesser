import { Airport, Message, Rules } from "./types";

export function validateGuess(
  rules: Rules,
  origin?: Airport,
  destination?: Airport,
): Message | null {
  const originMissing = rules.useOrigin && origin == null;
  const destinationMissing = rules.useDestination && destination == null;
  const bothMissing = originMissing && destinationMissing;
  const isInvalid = originMissing || destinationMissing;

  if (isInvalid) {
    if (bothMissing) {
      return {
        title: "Neither of the airports were provided",
        message:
          "To make a guess, provide guesses for the origin and destination airports.",
      };
    } else if (originMissing) {
      return {
        title: "An origin airport was not provided",
        message:
          "To make a guess, either provide an origin airport or disable origin guesses from the settings menu.",
      };
    } else if (destinationMissing) {
      return {
        title: "A destination airport was not provided",
        message:
          "To make a guess, either provide an destination airport or disable origin guesses from the settings menu.",
      };
    }
  }
  return null;
}
