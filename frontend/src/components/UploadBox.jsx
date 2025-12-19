import { useState } from "react";

export default function UploadBox() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");

    const res = await fetch("http://127.0.0.1:8000/api/upload", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      setStatus("Document uploaded successfully");
    } else {
      setStatus("Upload failed");
    }
  };

  return (
    <div className="card">
      <h3>Upload Document</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload</button>
      <p>{status}</p>
    </div>
  );
}
