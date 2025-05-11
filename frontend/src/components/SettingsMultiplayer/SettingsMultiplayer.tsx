import { FC, useState } from "react";
import "./SettingsMultiplayer.css";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner";
import PopupMenu from "../PopupMenu/PopupMenu";
import TextInput from "../TextInput/TextInput";
import { useGameStore } from "../../utils/gameStore";
import { useLobbyStore } from "../../utils/lobbyStore";

type JoinMode = "none" | "new" | "existing";

interface SettingsMultiplayerProps {
  onClose: () => void;
}

const SettingsMultiplayer: FC<SettingsMultiplayerProps> = ({ onClose }) => {
  const singleRules = useGameStore((state) => state.rules);
  const lobbyResponse = useLobbyStore((state) => state.lobbyResponse);
  const name = useLobbyStore((state) => state.name);
  const currentId = useLobbyStore((state) => state.lobbyId);
  const setName = useLobbyStore((state) => state.setName);
  const initLobby = useLobbyStore((state) => state.initLobby);
  const leaveLobby = useLobbyStore((state) => state.onLeaveLobby);

  const [joinMode, setJoinMode] = useState<JoinMode>("none");
  const [joinLobbyId, setJoinLobbyId] = useState(currentId ? currentId : "");

  return (
    <PopupMenu>
      <div className="settings-multiplayer">
        <h1>Multiplayer</h1>

        {lobbyResponse.status === "Loading" ? (
          <div className="settings-multiplayer-loading">
            <LoadingSpinner />
          </div>
        ) : lobbyResponse.status === "Ready" ? (
          <>
            <h3>Currently in lobby: {currentId}</h3>
            <h3>Name: {name}</h3>
            <div className="settings-multiplayer-option">
              <button onClick={() => leaveLobby()}>Leave Lobby</button>
            </div>
          </>
        ) : lobbyResponse.status === "Error" ? (
          <>
            <h2>{lobbyResponse.error?.title}</h2>
            <h4>{lobbyResponse.error?.message}</h4>
            <button onClick={() => leaveLobby()}>OK</button>
          </>
        ) : joinMode === "none" ? (
          <div className="settings-multiplayer-option">
            <button onClick={() => setJoinMode("new")}>Create Lobby</button>
            <button onClick={() => setJoinMode("existing")}>Join Lobby</button>
          </div>
        ) : (
          <>
            <div className="settings-multiplayer-option">
              <h3 className="settings-multiplayer-label">Name</h3>
              <TextInput value={name} setValue={setName} />
            </div>

            {joinMode === "existing" && (
              <>
                <div className="settings-multiplayer-option">
                  <h3 className="settings-multiplayer-label">Lobby ID</h3>
                  <TextInput value={joinLobbyId} setValue={setJoinLobbyId} />
                </div>
                <div className="settings-multiplayer-option">
                  <button
                    onClick={() => {
                      setJoinMode("none");
                      initLobby(joinLobbyId, singleRules);
                    }}
                    className="settings-multiplayer-highlight"
                  >
                    Join Lobby
                  </button>
                </div>
              </>
            )}

            {joinMode === "new" && (
              <div className="settings-multiplayer-option">
                <button
                  onClick={() => {
                    setJoinMode("none");
                    initLobby("", singleRules);
                  }}
                  className="settings-multiplayer-highlight"
                >
                  Create Lobby
                </button>
              </div>
            )}
          </>
        )}

        <div className="settings-multiplayer-option">
          {joinMode !== "none" && (
            <button onClick={() => setJoinMode("none")}>Back</button>
          )}
          <button
            className="settings-multiplayer-close"
            onClick={() => onClose()}
          >
            Done
          </button>
        </div>
      </div>
    </PopupMenu>
  );
};

export default SettingsMultiplayer;
