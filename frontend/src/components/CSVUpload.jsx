import { useState, useRef } from "react";
import api from "../services/api";

function CSVUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setMessage(`Selected: ${selectedFile.name}`);
      setUploadSuccess(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file.");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("file", file);

      await api.post(
        "/csv/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setUploadSuccess(true);
      setMessage(
        `File "${file.name}" uploaded successfully!`
      );

      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      if (onUploadSuccess) {
        onUploadSuccess();
      }

    } catch (error) {
      console.error(error);

      setUploadSuccess(false);

      setMessage(
        error.response?.data?.detail ||
        "Upload failed."
      );
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow mb-8">

      <h2 className="text-2xl font-semibold mb-4">
        Import Transactions
      </h2>

      {/* Hidden input */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="hidden"
      />

      {/* Drop Area */}
      <div
        onClick={() => fileInputRef.current.click()}
        className="
          border-2 border-dashed border-gray-300
          rounded-xl p-8
          text-center
          cursor-pointer
          hover:border-blue-500
          hover:bg-gray-50
          transition
        "
      >
        <p className="text-lg font-medium">
          Click to upload CSV
        </p>

        <p className="text-gray-500 mt-2">
          Drag & drop support coming soon
        </p>

        {file && (
          <p className="mt-4 text-blue-600 font-semibold">
            {file.name}
          </p>
        )}
      </div>

      {file && (
        <button
          onClick={handleUpload}
          className="
            mt-4 w-full
            bg-green-600
            text-white
            p-3 rounded-lg
            hover:bg-green-700
          "
        >
          Upload File
        </button>
      )}

      {message && (
        <div
          className={`
            mt-4 p-3 rounded-lg
            ${
              uploadSuccess
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }
          `}
        >
          {message}
        </div>
      )}

    </div>
  );
}

export default CSVUpload;