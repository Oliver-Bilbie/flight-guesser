import { FC, useState } from "react";
import "./SettingsMultiplayer.css";
import TextInput from "../TextInput/TextInput";
import { useLobbyStore } from "../../utils/lobbyStore";
import { useGameStore } from "../../utils/gameStore";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";

// TODO: Remove or use
// interface SettingsMultiplayerProps {
//   onClose: () => void;
// }

// const SettingsMultiplayer: FC<SettingsMultiplayerProps> = ({ onClose }) => {
const SettingsMultiplayer: FC = () => {
  const [doJoin, setDoJoin] = useState(false);
  const [joinLobbyId, setJoinLobbyId] = useState("");

  const singleRules = useGameStore((state) => state.rules);

  const lobbyResponse = useLobbyStore((state) => state.lobbyResponse);
  const name = useLobbyStore((state) => state.name);
  const currentId = useLobbyStore((state) => state.lobbyId);
  const setName = useLobbyStore((state) => state.setName);
  const initLobby = useLobbyStore((state) => state.initLobby);
  const leaveLobby = useLobbyStore((state) => state.onLeaveLobby);

  return (
    <div>
      {lobbyResponse.status === "Loading" ? (
        <LoadingSpinner />
      ) : lobbyResponse.status === "Ready" ? (
        <>
          <div className="settings-multiplayer-option">
            <h3>Currently in lobby: {currentId}</h3>
          </div>
          <div className="settings-multiplayer-option">
            <button onClick={() => leaveLobby()}>Leave Lobby</button>
          </div>
        </>
      ) : (
        <>
          <div className="settings-multiplayer-option">
            <h3>Name</h3>
            <TextInput value={name} setValue={setName} />
          </div>
          {doJoin ? (
            <>
              <div className="settings-multiplayer-option">
                <h3>Lobby ID</h3>
                <TextInput value={joinLobbyId} setValue={setJoinLobbyId} />
              </div>
              <div className="settings-multiplayer-option">
                <button onClick={() => initLobby(joinLobbyId, singleRules)}>
                  Join Lobby
                </button>
              </div>
            </>
          ) : (
            <div className="settings-multiplayer-option">
              <button onClick={() => initLobby("", singleRules)}>
                Create Lobby
              </button>
              <button onClick={() => setDoJoin(true)}>Join Lobby</button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SettingsMultiplayer;
