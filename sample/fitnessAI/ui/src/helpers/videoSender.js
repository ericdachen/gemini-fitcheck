import axios from "axios";

export async function getPresignedURL(fileName) {
    try {
        const response = await axios.post('http://127.0.0.1:8000/upload-url', {"file_name": fileName});
        return response['data'];
    } catch (error) {
        console.log(error);
    }
}

export async function putAudioIntoPresigned(presignedFields, audioBlob) {
    const formData = new FormData();

    Object.keys(presignedFields['fields']).forEach(key => {
        formData.append(key, presignedFields['fields'][key]);
    })

    formData.append('file', audioBlob);

    try {
        const response = await fetch(presignedFields.url, {
            method: 'POST',
            body: formData,
        })
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log('File successfully uploaded');

        return response;
    } catch (error) {
        console.error('Error uploading file:', error);
    }
}