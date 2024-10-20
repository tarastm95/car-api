import { useEffect, useState } from "react";
import { carService } from "../../services/carService";
import { socketService } from "../../services/socketService";

const Cars = () => {
    const [cars, setCars] = useState([]);
    const [trigger, setTrigger] = useState(null);

    useEffect(() => {
        carService.getAll().then(({ data }) => setCars(data.data)); // Access the 'data' array
    }, [trigger]);

    useEffect(() => {
        socketInit();
    }, []);

    const socketInit = async () => {
        const { cars } = await socketService();
        const client = await cars();

        client.onopen = () => {
            console.log('car socket connected');
            client.send(JSON.stringify({
                action: 'subscribe_to_car_activity',
                request_id: new Date().getTime()
            }));
        }

        client.onmessage = ({ data }) => {
            console.log(data);
            setTrigger(prev => !prev);
        }
    }

    return (
        <div>
            {cars.map(car => (
                <div key={car.id}> {/* Added a key prop for each car */}
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
                    <hr />
                </div>
            ))}
        </div>
    );
};

export { Cars };
