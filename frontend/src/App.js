import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [cars, setCars] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('/api/cars')
            .then(({ data }) => {
                console.log("Received data:", data); // Логування отриманих даних
                // Тепер використовуємо data.data, щоб отримати масив автомобілів
                if (Array.isArray(data.data)) {
                    setCars(data.data); // Якщо дані — це масив
                } else {
                    setError("Invalid data format");
                }
            })
            .catch((error) => {
                console.error("There was an error fetching the cars!", error);
                setError("Failed to fetch cars");
            });
    }, []);

    return (
        <div className="App">
            {error && <div className="error">{error}</div>}
            {Array.isArray(cars) && cars.length > 0 ? (
                cars.map(car => (
                    <div key={car.id}>{JSON.stringify(car)}</div>
                ))
            ) : (
                <div>No cars were found, or the data is in the incorrect format.</div>
            )}
        </div>
    );
}

export default App;
