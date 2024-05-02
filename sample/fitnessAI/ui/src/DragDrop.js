import React, { useRef, useState } from 'react';
import './App.css';

const DragDropArea = () => {
  const fileInputRef = useRef(null);
  const [ fileName, setFileName ] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const files = e.dataTransfer.files;
    handleFiles(files);
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    handleFiles(files);
  };

  const handleFiles = (files) => {
    // Handle the dropped or selected files here
    console.log(files);
    if (files[0]) {
        setFileName(files[0]['name'])
    }
  };

  return (
    <div
      className="drag-drop-area"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <p>Drag and drop videos here or click to select files</p>
      {fileName && <p> {fileName} </p>}
    </div>
  );
};

export default DragDropArea;