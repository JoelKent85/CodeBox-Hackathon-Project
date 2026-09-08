import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("What do you need help with today?");

  const sendToBackend = () => {
    fetch("https://codebox-hackathon-project.onrender.com/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text
      }),
    }).then(response => response.json())
      .then(data => { setResponse(data.response) })
  }

  return (
    <div>
      <h1>Cal Poly Finder</h1>
      <div className="response-container">
        <ReactMarkdown>{response}</ReactMarkdown>
      </div>
      <div className="prompt-container">
        <input 
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendToBackend();
              setResponse("Loading...")
              setText("");
            }
          }}
        />
      </div>
    </div>
  );
}

export default App;