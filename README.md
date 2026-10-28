# Flight Guesser

Flight Guesser is a game based on your real-world location. Guess the airport the nearest plane is flying to or from, and score points for how close you were. Positions and routes come from [Flightradar24](https://www.flightradar24.com/).

[**Play it here**](https://flights.oliver-bilbie.co.uk)

There are no accounts. A singleplayer score stays in the browser and can be reset from settings. For multiplayer games, create a lobby and share its four-letter code, or join someone else's. The host's origin and destination settings are enforced for the room. Your score is stored against your name in that lobby, and it comes back if you rejoin with the same name. The leaderboard updates in real-time as guesses are made.

## Scoring

Each enabled guess is worth up to 100 points. The score decays exponentially with distance, so a neighbouring airport is still a strong guess but a different continent is not. If no airport data is available, that guess awards nothing, and the available flight details are still shown.

## How it works

The site is a React app (Vite, TypeScript, Zustand, Leaflet) on S3, served through CloudFront. Singleplayer guesses are a POST to an HTTP API. Multiplayer is an API Gateway WebSocket, so lobby changes can be pushed instead of polled.

Both game Lambdas are dependency-free Python and share the guess logic in `backend/src/helpers`. Lobby and player rows live in DynamoDB. A third Lambda refreshes `airports.json` in the site bucket once a day which contains a fresh list of all airports in the world from which guesses can be made. Infrastructure is defined in Terraform for reproducible deployment to AWS.

```text
frontend/     React app
backend/      Lambda handlers and shared guess logic
terraform/    AWS infrastructure
deploy.sh     Package the Lambdas, apply Terraform, publish the site
```

## Local development

API URLs are not committed. `frontend/src/utils/endpoints.ts` holds placeholders. `deploy.sh` substitutes the Terraform outputs before the production build, then puts the placeholders back.

```bash
cd frontend
npm install
npm run dev
```

That serves the UI only. Guesses, lobbies, and the airport list need a deployed stack, with those placeholders replaced by real endpoints.

## Deploying

Deployment requires AWS CLI, Terraform, and Node.

```bash
export STAGE=dev   # or prd
./deploy.sh
```

`STAGE` selects `terraform/environments/$STAGE`. The script packages the three Lambdas, applies the stack, builds the frontend against that stage's endpoints, syncs the build to S3, and invalidates the CloudFront cache.
