# Changelog

## 1.10.0

### Changed

- Refined pop-up menu styling for improved visual clarity and consistency

## 1.9.0

### Changed

- Major UI theme overhaul to modernize the visual identity

## 1.8.0

### Added

- Introduced and expanded backend unit and integration test coverage

### Changed

- Enhanced linting rules for code quality
- Optimized build and test workflows for better performance

## 1.7.0

### Changed

- Cleaned and streamlined deployment pipeline definitions

## 1.6.1

### Changed

- Refactored deployment pipelines to use Infrastructure as Code (see [Pipelines](https://github.com/Oliver-Bilbie/pipelines))

## 1.6.0

### Added

- Scoring system updated to use exponential decay, making results more forgiving over longer distances
- Game rules defined by the host are now enforced across multiplayer lobbies
- Previously guessed flight IDs are stored in DynamoDB to avoid duplicate guesses across sessions
- DynamoDB restructured to use separate tables for player and lobby data
- Scoreboard now refreshes every 30 seconds automatically (if data saver mode is off)

## 1.5.0

### Added

- Backend now validates user input to help mitigate injection attacks

### Fixed

- CI pipeline now invalidates CloudFront cache after frontend deployment

## 1.4.2

### Updated

- Improved README content
- Added pipeline status badge to README
- Updated project dependencies

## 1.4.1

### Changed

- Migrated application to a new domain
- Updated dependencies

## 1.4.0

### Added

- CI/CD pipelines for automated deployment
  - Terraform modules for provisioning DynamoDB
  - Build scripts for frontend, backend, and infrastructure components
  - Development environment auto-deployment on pull request
  - Automated testing pipeline for PRs
  - Production deployment pipeline triggered on merge to `main`

## 1.3.1

### Security

- Upgraded backend runtime from Python 3.7 to 3.9
- Updated frontend package dependencies

## 1.3.0

### Added

- Support for multiplayer lobbies via DynamoDB
  - Players can now create and join lobbies from the settings menu
  - Lobby leaderboard displays scores for all current members
  - Rejoining with the same name restores the player’s previous state
  - Inactive players are automatically removed after 24 hours

## 1.2.2

### Changed

- Backend now strips escape characters from airport names

## 1.2.1

### Changed

- Improved responsiveness and layout for smaller screens

## 1.2.0

### Added

#### Frontend

- New `SettingsMenu` component
- Inputs for guessing origin, destination, or both

#### Backend

- Support for handling origin-based guesses
- Renamed `airport` fields to `destination` for clarity

## 1.1.5

### Fixed

- Resolved API response handling issues

## 1.1.4

### Added

- Initial frontend test suite

## 1.1.3

### Changed

- Migrated frontend from JavaScript to TypeScript

## 1.1.2

### Changed

- Refactored backend for modularity
- Achieved 100% unit and integration test coverage for the backend
- Frontend now performs fewer API requests

## 1.1.1

### Changed

- UI layout and styling improvements

## 1.1.0

### Added

- Ability to guess the flight’s destination airport and receive score based on proximity

## 1.0.0

### Added

- Initial public release
