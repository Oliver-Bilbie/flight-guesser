import { ReactElement, useState, useRef } from "react";
import "./Selector.css";

interface SelectorProps<T> {
  items: T[];
  charsBeforeSearch?: number;
  displayItem?: (item: T) => string;
  onSelect: (item: T) => void;
}

const Selector = <T,>({
  items,
  charsBeforeSearch = 3,
  displayItem = (item) => String(item),
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
    onSelect(undefined as T);
  };

  const handleItemClick = (item: T) => {
    setInputText(displayItem(item));
    setSelected(true);
    onSelect(item);
    setShowDropdown(false);
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
          displayItem(item).toLowerCase().includes(inputText.toLowerCase()),
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
                {displayItem(item)}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Selector;
