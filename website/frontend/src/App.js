// App.jsx or App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult("");
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data.prediction === 1 ? "Malicious" : "Benign");
    } catch (err) {
      console.error(err);
      setResult("Error occurred during prediction.");
    }
  };

  return (
    <div className="App" style={{ padding: 20 }}>
      <h1>PDF Malware Detector</h1>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleSubmit} style={{ marginTop: 10 }}>Submit</button>
      {result && <p><strong>Prediction:</strong> {result}</p>}
    </div>
  );
}

export default App;
