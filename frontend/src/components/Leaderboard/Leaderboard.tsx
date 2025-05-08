import { FC } from "react";
import "./Leaderboard.css";
import { useLobbyStore } from "../../utils/lobbyStore";

function averageScore(score: number, guesses: number) {
  if (guesses === 0) {
    return 0;
  }
  return score / guesses;
}

const Leaderboard: FC = () => {
  const isMultiplayer =
    useLobbyStore((state) => state.lobbyResponse.status) === "Ready";
  const lobbyId = useLobbyStore((state) => state.lobbyId);
  const playerName = useLobbyStore((state) => state.name);
  const players = useLobbyStore((state) => state.players);

  const sortedPlayers = players.sort((a, b) => {
    const scoreDiff = b.score - a.score;
    if (scoreDiff !== 0) {
      return scoreDiff;
    }

    const averageDiff =
      averageScore(b.score, b.guess_count) -
      averageScore(a.score, a.guess_count);
    return averageDiff;
  });

  return (
    isMultiplayer && (
      <div className="leaderboard">
        <h2>Lobby ID: {lobbyId}</h2>
        {sortedPlayers.length > 0 && (
          <>
            <div className="leaderboard-header">
              <h4 className="leaderboard-item-name">Name</h4>
              <h4 className="leaderboard-item-score">Score</h4>
              <h4 className="leaderboard-item-average">Average</h4>
            </div>

            {sortedPlayers.map((player) => {
              return (
                <div
                  className={`leaderboard${player.player_name === playerName ? "-current" : ""}-player`}
                  key={player.player_name}
                >
                  <h4 className="leaderboard-item-name">
                    {player.player_name}
                  </h4>
                  <h4 className="leaderboard-item-score">{player.score}</h4>
                  <h4 className="leaderboard-item-average">
                    {averageScore(player.score, player.guess_count)}
                  </h4>
                </div>
              );
            })}
          </>
        )}
      </div>
    )
  );
};

export default Leaderboard;
