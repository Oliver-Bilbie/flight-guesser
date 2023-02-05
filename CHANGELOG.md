# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## 1.6.1

### Updated

- Reworked pipelines as IaC (see [Pipelines](https://github.com/Oliver-Bilbie/pipelines))

## 1.6.0

### Added

- Scoring has been reworked to follow an exponential decay, making it slightly more generous for further away guesses
- The host's game settings are now enforced for all players in a multiplayer lobby
- Previously guessed flight IDs are now stored in the DynamoDB table to prevent duplicated guesses across multiple sessions
- The dynamoDB configuration have been reworked to store player data and lobby data in seperate tables
- The scoreboard will now refresh automatically every thirty seconds if data-saver is disabled

## 1.5.0

### Added

- The backend will now validate user inputs to reduce the potential for code-injection attacks

### Fixed

- The ci script will now invalidate the CloudFront cache once the new frontend has been deployed to S3

## 1.4.2

### Updated

- Updated README
- Added a badge to README to indicate pipeline status
- Updated dependencies

## 1.4.1

### Updated

- Migrated to a new domain name
- Updated dependencies

## 1.4.0

### Added

- Added CI/CD Pipelines to automatically deploy the application
    - Added terraform modules to build the DynamoDB table
    - Added build scripts for use by corresponding AWS CodeBuild projects
    - CodeBuild will now deploy the terraform, frontend, and backend into a development environment upon creating a pull request
    - CodeBuild will now run tests upon creating a pull request
    - CodeBuild will now deploy the terraform, frontend, and backend into a production environment upon merge into main

## 1.3.1

### Security

- Updated backend from Python 3.7 to 3.9
- Updated frontend dependencies

## 1.3.0

### Added

- Added support for multiplayer lobbies using DynamoDB
    - Players may now create or join a lobby from the settings menu.
    - Whilst a player is a member of a lobby, a leaderboard will be displayed for all players in the same lobby.
    - Players may re-join a lobby using the same name to assume their previous score.
    - Inactive players will be removed from lobbies after 24 hours.

## 1.2.2

### Changed

- Added a backend function to remove escape characters from airport names

## 1.2.1

### Changed

- Improved UI on small displays

## 1.2.0

### Added

#### Frontend

- Added SettingsMenu component
- Added inputs for guessing an origin, destination, or both

#### Backend

- Added handling for origin guesses
- Changed naming convention for destination airports from "airport" to "destination"

## 1.1.5

### Fixed

- Fixed API response handling

## 1.1.4

### Changed

- Added frontend tests

## 1.1.3

### Changed

- Converted frontend from JavaScript into TypeScript

## 1.1.2

### Added

- Refactored backend
- 100% backend unit test coverage
- 100% backend integration test coverage
- Refactored frontend
- Frontend now makes fewer API calls

## 1.1.1

### Changed

- UI Tidying

## 1.1.0

### Added

- Added the ability to guess which airport a plane is travelling to, and score points based on proximity to the true location.

## 1.0.0

### Added

- Initial build
