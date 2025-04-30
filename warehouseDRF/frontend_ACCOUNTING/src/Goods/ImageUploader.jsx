import React, { useState } from 'react';
import axios from 'axios';
import GroupsAll from "./Groups"



const ImageUploader = () => {
    const [files, setFiles] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [results, setResults] = useState(null);

    const handleFileChange = (e) => {
        setFiles(Array.from(e.target.files)); // Конвертируем FileList в массив
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (files.length === 0) return;

        setIsUploading(true);
        const formData = new FormData();
        
        // Добавляем все файлы в FormData
        files.forEach((file, index) => {
            formData.append(`image_${index}`, file); // Ключи могут быть любыми
        });

        try {
            const response = await axios.post(
                'http://127.0.0.1:9999/api/upload-images/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            
            setResults(response.data);
        } catch (error) {
            console.error('Upload error:', error);
            setResults({
                error: 'Failed to upload files',
                details: error.response?.data
            });
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div>
            <GroupsAll />


            <h2>Массовая загрузка фото</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleFileChange}
                    disabled={isUploading}
                />
                <button type="submit" disabled={isUploading || files.length === 0}>
                    {isUploading ? 'Загрузка...' : `Загрузить ${files.length} файлов`}
                </button>
            </form>

            {results && (
                <div>
                    <h3>Результаты:</h3>
                    <p>Успешно загружено: {results.total_uploaded}</p>
                    
                    {results.errors?.length > 0 && (
                        <div style={{ color: 'red' }}>
                            <h4>Ошибки:</h4>
                            <ul>
                                {results.errors.map((err, i) => (
                                    <li key={i}>{err.name}: {err.error}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    
                    <div>
                        <h4>Загруженные файлы:</h4>
                        <ul>
                            {results.saved_files?.map((file, i) => (
                                <li key={i}>
                                    <a href={file.url} target="_blank" rel="noopener noreferrer">
                                        {file.name} ({Math.round(file.size / 1024)} KB)
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageUploader;