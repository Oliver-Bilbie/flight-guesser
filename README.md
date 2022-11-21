# Flight Guesser
[![Site-Up](https://img.shields.io/website?url=https%3A%2F%2Fflight-guesser.net%2F)](https://flight-guesser.net)

[![Last-Commit](https://img.shields.io/github/last-commit/Oliver-Bilbie/flight-guesser)](https://github.com/Oliver-Bilbie/flight-guesser/blob/main/CHANGELOG.MD)

---

## Overview
When you see an aircraft overhead, you may use the flight-guesser application to guess the destination of the aircraft.
You will score points based on accuracy. Data is sourced from FlightRadar24 using [FlightRadarAPI](https://github.com/JeanExtreme002/FlightRadarAPI).

### [Hosted here](https://flight-guesser.net)

---

## Architecture
### Frontend
The frontend is written using [React](https://reactjs.org/) with the code written in TypeScript. I have used the [Grommet](https://v2.grommet.io/) component library for UI elements as well as icons.
The frontend is hosted from an [AWS S3](https://aws.amazon.com/s3/) bucket using the static website hosting functionality. This service does not support HTTPS connections, so I have used an [AWS Cloudfront](https://aws.amazon.com/cloudfront/) distribution along with AWS's certificate manager to provide this functionality.

### Backend
The backend is written in Python 3.9 and is deployed as a set of [AWS Lambda](https://aws.amazon.com/lambda/) functions. The deployment is handled using [Serverless Framework](https://www.serverless.com/framework/) along with the [Serverless Python Requirements](https://www.serverless.com/plugins/serverless-python-requirements) and [Serverless IAM Roles Per Function](https://www.serverless.com/plugins/serverless-iam-roles-per-function) plugins. The Serverless Python Requirements plugin is used to create a Lambda layer with the required Pip dependencies which is driven from the backend Pipfile, and the Serverless IAM Roles Per Function plugin is used to conveniently control IAM permissions on a per-function basis.
The backend uses a [DynamoDB](https://aws.amazon.com/dynamodb/) table to handle multiplayer functionality.

### Pipelines
When a PR is created or updated, a [CodeBuild](https://aws.amazon.com/codebuild/) event is triggered which will deploy the project into a development environment, and a second event which will run the unit and integration tests. A merge into the main branch will trigger an event which will deploy the project into the production environment.

For this project I have decided to use one of AWS's default build images, since I do not have the time to consistently maintain my own. As a result, the dependencies are installed each time a build is run which is not ideal, but this works well enough for now.

The pipelines will build the required DynamoDB table using [Terraform](https://www.terraform.io/), deploy the backend using [Serverless Framework](https://www.serverless.com/framework/), and then finally build the frontend and copy the files to [AWS S3](https://aws.amazon.com/s3/).

---

## To Do
-   Set game rules for lobby members to match those of the host
-   Log guessed flights for each player to the database to avoid cheating
-   Improve input validation
-   Automatically fetch lobby data periodically when data saver is turned off
-   Allow aircraft model guesses
-   Retrieve additional flight data if data saver is turned off
-   Redesign the dynamo table to use composite keys
-   Use IAM to only allow API calls originating from the frontend
-   Refactoring and tidying
-   Write and update tests
-   Update Documentation
