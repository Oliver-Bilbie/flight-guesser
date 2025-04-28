import { ReactElement, useState, useRef } from "react";
import "./Selector.css";

interface SelectorProps<T> {
  items: T[];
  charsBeforeSearch?: number;
  onSelect: (item: T) => void;
}

const Selector = <T,>({
  items,
  charsBeforeSearch = 3,
  onSelect,
}: SelectorProps<T>): ReactElement => {
  const [inputText, setInputText] = useState<string>("");
  const [touched, setTouched] = useState<boolean>(false);
  const [selected, setSelected] = useState<boolean>(false);
  const [showDropdown, setShowDropdown] = useState<boolean>(false);

  const inputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(e.target.value);
    setSelected(false);
  };

  const handleItemClick = (item: T) => {
    const displayText = String(item);
    setInputText(displayText);
    setSelected(true);
    setShowDropdown(false);
    onSelect(item);
    inputRef.current?.blur();
  };

  const handleBlur = () => {
    setTouched(true);
    // Slight delay to allow button clicks to register
    setTimeout(() => setShowDropdown(false), 100);
  };

  const handleFocus = () => {
    setShowDropdown(true);
  };

  const filteredItems =
    inputText.length >= charsBeforeSearch
      ? items.filter((item) =>
          String(item).toLowerCase().includes(inputText.toLowerCase()),
        )
      : [];

  const hasError = inputText.length > 0 && touched && !selected;

  return (
    <div className="selector">
      <input
        ref={inputRef}
        className={`selector-input ${hasError ? "selector-input-error" : ""}`}
        type="text"
        value={inputText}
        onChange={handleInputChange}
        onBlur={handleBlur}
        onFocus={handleFocus}
        placeholder="Type to search..."
      />
      {inputText.length > 0 && showDropdown && (
        <div className="selector-content">
          {filteredItems.map((item, index) => {
            const displayText = String(item);
            return (
              <button
                type="button"
                className="selector-option"
                key={index}
                onMouseDown={(event) => {
                  event.preventDefault();
                  handleItemClick(item);
                }}
              >
                {displayText}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Selector;
