// components/SearchBar.js
import React from 'react';

const SearchBox = ({ searchTerm, onSearchChange, onSearchSubmit }) => {
  return (
    <div className="search-box">
      <form onSubmit={onSearchSubmit}>
        <input
          type="text"
          placeholder="Введите название товара..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Найти
        </button>
      </form>
    </div>
  );
};

export default SearchBox;