import { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
    const [cars, setCars] = useState([]);

    useEffect(() => {
        axios.get('/api/cars').then(({ data }) => {
            setCars(data.data); // Access the 'data' array within the response
        });
    }, []);

    return (
        <div>
            <h1>Cars</h1>
            {cars.length > 0 ? (
                cars.map(car => (
                    <div key={car.id} style={{ marginBottom: '20px', border: '1px solid #ccc', padding: '10px' }}>
                        <h3>{car.model} ({car.year})</h3>
                        <p>Body Type: {car.body_type}</p>
                        <p>Price: ${car.price}</p>
                        {car.photos.length > 0 && (
                            <div>
                                <h4>Photos:</h4>
                                {car.photos.map((photo, index) => (
                                    <img
                                        key={index}
                                        src={photo.photo}
                                        alt={`${car.model} - ${index + 1}`}
                                        style={{ width: '100px', margin: '5px' }}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                ))
            ) : (
                <p>No cars available</p> // Message if no cars are present
            )}
        </div>
    );
};

export { App };
