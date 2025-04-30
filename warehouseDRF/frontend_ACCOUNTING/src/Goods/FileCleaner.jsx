import React, { useState } from 'react';
import axios from 'axios';
import GroupsAll from "./Groups"


const FileCleaner = () => {
    const [isCleaning, setIsCleaning] = useState(false);
    const [results, setResults] = useState(null);

    const handleCleanFiles = async () => {
        if (!window.confirm('Вы уверены, что хотите удалить все неиспользуемые файлы?')) {
            return;
        }

        setIsCleaning(true);
        try {
            const response = await axios.get('http://127.0.0.1:9999/api/clean-unused-files/');
            setResults(response.data);
        } catch (error) {
            console.error('Ошибка при очистке файлов:', error);
            setResults({
                error: 'Не удалось очистить файлы',
                details: error.response?.data
            });
        } finally {
            setIsCleaning(false);
        }
    };

    return (
        <div>

            <GroupsAll />

            <h2>Очистка неиспользуемых файлов</h2>
            <button 
                onClick={handleCleanFiles} 
                disabled={isCleaning}
                style={{ backgroundColor: isCleaning ? '#ccc' : '#ff4444', color: 'white' }}
            >
                {isCleaning ? 'Идет очистка...' : 'Удалить неиспользуемые файлы'}
            </button>

            {results && (
                <div style={{ marginTop: '20px' }}>
                    <h3>Результаты:</h3>
                    <p>Удалено файлов: {results.total_deleted}</p>
                    
                    {results.errors?.length > 0 && (
                        <div style={{ color: 'red' }}>
                            <h4>Ошибки:</h4>
                            <ul>
                                {results.errors.map((err, i) => (
                                    <li key={i}>{err.file}: {err.error}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    
                    {results.deleted_files?.length > 0 && (
                        <div>
                            <h4>Удаленные файлы:</h4>
                            <ul>
                                {results.deleted_files.map((file, i) => (
                                    <li key={i}>{file}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default FileCleaner;