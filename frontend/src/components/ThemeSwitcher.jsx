import React from "react";

export default function ThemeSwitcher({ onSwitch, theme }) {
  return (
    <button onClick={onSwitch} className="theme-toggle-btn">
      {theme === "light" ? "🌙 Темная" : "☀️ Светлая"}
    </button>
  );
}