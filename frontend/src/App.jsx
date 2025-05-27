import React, { useState, useRef, useEffect } from "react";
import { marked } from "marked";


function App() {
  const [theme, setTheme] = useState("light");
  const [prompt, setPrompt] = useState("");
  const [fileName, setFileName] = useState("");
  const [fileContent, setFileContent] = useState("");
  const responseContainerRef = useRef(null);
  const [loadingMsgId, setLoadingMsgId] = useState(null);

  // Apply selected theme
  useEffect(() => {
    const stylesheet = document.getElementById("themeStylesheet");
    if (stylesheet) {
      stylesheet.href = `/static/${theme}.css`;
    }
  }, [theme]);

  // Greeting message on load
  useEffect(() => {
    const greeting = "Привет👋 Я ассистент PostgreSQL. Я могу помочь с составлением отчета по инциденту или найти решение проблеме, связанной с PostgreSQL. Просто загрузи файл или задай вопрос";
    animateMessage("giga", greeting);
  }, []);

  const handleThemeSwitch = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    const text = await file.text();
    setFileContent(text);
  };

  const addMessage = (role, content) => {
    const container = responseContainerRef.current;
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}-message`;
    msgDiv.innerHTML = content; // <--- Now supports HTML, including parsed Markdown
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
  };

  const animateMessage = async (role, content, delay = 40) => {
    const container = responseContainerRef.current;
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}-message`;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
  
    const words = content.split(" ");
    for (let word of words) {
      msgDiv.innerHTML += word + " ";
      container.scrollTop = container.scrollHeight;
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  };

  const handleSubmit = async () => {
    if (!prompt && !fileContent) return;
  
    addMessage("user", prompt);
    setPrompt("");
  
    const formData = new FormData();
    formData.append("prompt", prompt);
    if (fileContent) {
      const blob = new Blob([fileContent], { type: "text/plain" });
      formData.append("file", blob, fileName);
    }
  
    const tempId = Date.now();
    setLoadingMsgId(tempId);
  
    const container = responseContainerRef.current;
    const msgDiv = document.createElement("div");
    msgDiv.className = "message giga-message loading";
    msgDiv.id = `loading-${tempId}`;
    msgDiv.innerHTML = `<span class="dots">Обрабатываю запрос<span>.</span><span>.</span><span>.</span></span>`;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
  
    const res = await fetch("/get_incident_report/", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
  
    // Remove loading message before showing result
    const existingLoader = document.getElementById(`loading-${tempId}`);
    if (existingLoader) existingLoader.remove();
    setLoadingMsgId(null);
  
    // Render full structured report
    if (data.incident_summary && data.incident_type && data.root_cause && data.solution) {
      const reportHTML = `
        <div class="report">
          <h2>Отчёт по инциденту</h2>
          <div class="summary">
            <h4>Краткое резюме</h4>
            <p>${data.incident_summary}</p>
          </div>
          <div class="incident-type">
            <h4>Тип инцидента</h4>
            <p>${data.incident_type}</p>
          </div>
          <div class="root-cause">
            <h4>Корневая причина</h4>
            <p>${data.root_cause}</p>
          </div>
          <div class="solution">
            <h4>Решение</h4>
            ${marked.parse(data.solution)}
          </div>
        </div>
      `;
      addMessage("giga", reportHTML);
      setFileName("");
      setFileContent("");
    } else if (data.solution) {
      const solutionHTML = marked.parse(`### 🛠️ Решение\n\n${data.solution}`);
      addMessage("giga", solutionHTML);
    } else {
      const fallback = marked.parse(JSON.stringify(data, null, 2));
      addMessage("giga", fallback);
    }
  };

  return (
    <>
      <link
        id="themeStylesheet"
        rel="stylesheet"
        href={`/static/${theme}.css`}
      />
      <a href="/" className="home">
        <img src="/static/main.png" alt="Home" />
      </a>

      <div className="container-ask">
        <div id="responseContainer" ref={responseContainerRef} className="response-container"></div>

        <div className="input-container">
          <label htmlFor="fileInput" className="icon icon-left">
            <img src="/static/attachment.png" className="img-left" alt="Attach" />
          </label>
          <input type="file" id="fileInput" onChange={handleFileUpload} style={{ display: "none" }} />
          <input
            type="text"
            id="userPrompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Введи свой запрос"
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />
          <img
            src="/static/up-arrow.png"
            alt="Send"
            className="img-right"
            onClick={handleSubmit}
          />
        </div>
        <div className="file-name-display">{fileName}</div>
      </div>

      <div className="theme-switcher">
        <img
          src={`/static/${theme === "light" ? "day-and-night.png" : "day-and-night-light.png"}`}
          id="switchThemeBtn"
          alt="Switch Theme"
          onClick={handleThemeSwitch}
        />
      </div>
    </>
  );
}

export default App;