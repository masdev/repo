import { useLoaderData } from "react-router-dom"
import CarCard from "../components/CarCard"

const Cars = () => {
    const cars = useLoaderData()
    return (
        <div>
            <h2>Available Cars</h2>
            <div className="md:grid md:grid-cols-3 sm:grid sm:grid-cols-2 gap-5">
                {cars === undefined || cars.length === 0 ? (
                    <h2>No Data!</h2>
                ) : (
                    cars.map(car => (
                        <CarCard key={car._id || car.id} car={car} />
                    ))
                )}
            </div>
        </div>
    )
};

/** ` */
export const carsLoader = async () => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/cars?limit=30`);
    
    const response = await res.json()
    if (!res.ok) {
        throw new Error(response.message)
    }
    
    return response["cars"]
}

export default Cars

