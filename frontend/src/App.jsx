import { useState } from "react";
import UploadBox from "./components/UploadBox";
import QueryBox from "./components/QueryBox";
import AnswerBox from "./components/AnswerBox";
import "./App.css";

function App() {
  const [answer, setAnswer] = useState("");

  return (
    <div className="app-container">
      <h1>Smart Compliance Assistant</h1>

      <UploadBox />
      <QueryBox setAnswer={setAnswer} />
      <AnswerBox answer={answer} />
    </div>
  );
}

export default App;
