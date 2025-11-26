from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Request, status
from models import CarModel, CarCollection

router = APIRouter()

#http POST http://127.0.0.1:8000/cars/ brand="KIA" make="ceed" year=2001 cm3=2000 km=3000 price=18000
@router.post("/", response_description="Add new car", response_model=CarModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_car(request: Request, car: CarModel=Body(...)):
    cars = request.app.db["cars"]
    document = car.model_dump(by_alias=True, exclude=["id"])
    inserted = await cars.insert_one(document)
    return await cars.find_one({"_id": inserted.inserted_id})

#chapter7 % http http://127.0.0.1:8000/cars/
@router.get("/", response_description="Return all cars", response_model=CarCollection, response_model_by_alias=False)
async def list_cars(request: Request):
    cars = request.app.db["cars"]
    results = []
    cursor = cars.find()
    async for document in cursor:
        results.append(document)
    return CarCollection(cars=results)

#chapter7 % http http://127.0.0.1:8000/cars/
@router.get("/{id}", response_description="Find car by ID", response_model=CarModel, response_model_by_alias=False)
async def find_car_by_id(request: Request, id: str):
    cars = request.app.db["cars"]
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Car with {id} not found")

    if (car := await cars.find_one({"_id": ObjectId(id)})) is not None:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Car with {id} not found")
    
