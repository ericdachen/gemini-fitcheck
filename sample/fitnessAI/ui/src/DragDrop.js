import React, { useRef, useState } from 'react';
import './App.css';
import { getPresignedURL, putAudioIntoPresigned } from './helpers/videoSender';

const DragDropArea = () => {
  const fileInputRef = useRef(null);
  const [ file, setFile ] = useState(null);


  const handleSubmit = () => {
    console.log(file)
    const reader = new FileReader();
    reader.onload = async (event) => {
        const blob = new Blob([reader.result], { type: file.type });
        const presignedFields = await getPresignedURL(file.name);
        await putAudioIntoPresigned(presignedFields, blob);
    };
    reader.readAsArrayBuffer(file[0]);
  }

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
        setFile(files)
    }
  };

  return (
    <>
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
        {file && <p> {file[0]['name']} </p>}
        </div>
        {file && <button onClick={()=>handleSubmit()}> Submit </button>}
    </>
  );
};

export default DragDropArea;