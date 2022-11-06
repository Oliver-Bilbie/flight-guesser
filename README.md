# flight-guesser

The flight-guesser repository contains the frontend and backend source code for the flight-guesser application.

When you see an aircraft overhead, you may use the flight-guesser application to guess the destination of the aircraft.
You will score points based on accuracy. Data is sourced from FlightRadar24 using [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI).

[Hosted here](https://flight-guesser.net)

## To Do
-   Set game rules for lobby members to match those of the host
-   Log guessed flights for each player to the database to avoid cheating
-   Improve input validation
-   Fix stalling on first location request
-   Automatically fetch lobby data periodically when data saver is off
-   Refactoring
-   Write and update tests
-   Retrieve additional flight data if data saver is off
-   Redesign the dynamo table to use composite keys
-   Documentation
