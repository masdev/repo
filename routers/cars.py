import cloudinary
from cloudinary import uploader #noqa F401
from bson import ObjectId
from fastapi import (
    APIRouter,
    Depends,
    Form,
    Body,
    File,
    HTTPException,
    Request,
    status,
    UploadFile
    )
from fastapi.responses import Response
from pymongo import ReturnDocument
from models import (
    CarCollectionPagination, 
    CarModel, 
    CarCollection, 
    UpdateCarModel
)
from config import BaseConfig
CARS_PER_PAGE = 10

from authentication import AuthHandler

settings = BaseConfig()
router = APIRouter()
auth_handler = AuthHandler()
cloudinary.config(api_secret=settings.CLOUDINARY_SECRET_KEY,
    api_key=settings.CLOUDINARY_API_KEY,
    cloud_name=settings.CLOUDINARY_CLOUD_NAME)

#http POST http://127.0.0.1:8000/cars/ brand="KIA" make="ceed" year=2001 cm3=2000 km=3000 price=18000
#@router.post("/", response_description="Add new car", response_model=CarModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
#async def add_car(request: Request, car: CarModel=Body(...)):
#    cars = request.app.db["cars"]
#    document = car.model_dump(by_alias=True, exclude=["id"])
#    inserted = await cars.insert_one(document)
#    return await cars.find_one({"_id": inserted.inserted_id})


#(venv7) developer@amicos-MacBook-Pro chapter7 % http --form POST http://127.0.0.1:8000/cars/ brand="Fordyaka" make="classniy" year=2000 cm3=1500 km=90000 price=7000 picture@car.jpg 
@router.post("/", response_description="Add new car with picture", response_model=CarModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_car_with_picture(
    request: Request, 
    brand: str = Form("brand"),
    make: str = Form("make"),
    year: int = Form("year"),
    cm3: int = Form("cm3"),
    km: int = Form("km"),
    price: int = Form("price"),
    picture: UploadFile = File("picture")
    ):
    
    # Upload to Cloudinary
    try:
        cloudinary_image = cloudinary.uploader.upload(
            picture.file,
            crop="fill",
            width=800,
            folder="cars"
        )
        picture_url = cloudinary_image["url"]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image to Cloudinary: {str(e)}"
        )

    #create car model and save it in MongoDB
    car = CarModel(
        brand=brand,
        make=make,
        year=year,
        cm3=cm3,
        km=km,
        price=price,
        picture_url=picture_url
    )

    cars = request.app.db["cars"]
    document = car.model_dump(by_alias=True, exclude=["id"])

    inserted = await cars.insert_one(document)
    return await cars.find_one({"_id": inserted.inserted_id})

#chapter7 % http http://127.0.0.1:8000/cars/
#@router.get("/", response_description="Return all cars", response_model=CarCollection, response_model_by_alias=False)
#async def list_cars(request: Request):
#    cars = request.app.db["cars"]
#    results = []
#    cursor = cars.find()
#    async for document in cursor:
#        results.append(document)
#    return CarCollection(cars=results)

#chapter7 % http http://127.0.0.1:8000/cars/
@router.get("/", response_description="Return all cars, paginated", response_model=CarCollectionPagination, response_model_by_alias=False)
async def list_cars(request: Request, page: int = 1, limit: int = CARS_PER_PAGE):
    cars = request.app.db["cars"]
    results = [] 
    cursor = cars.find().sort("brand").limit(limit).skip((page - 1) * limit)

    total_documents = await cars.count_documents({})
    has_more = total_documents > limit * page

    async for document in cursor:
        results.append(document)

    return CarCollectionPagination(cars=results, page=page, has_more=has_more)

#chapter7 % http http://127.0.0.1:8000/cars/fasdj4355jdsgsdfg89j
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

#chapter7 % http http://127.0.0.1:8000/cars/fasdj4355jdsgsdfg89j
@router.put("/{id}", response_description="Update car by ID", response_model=CarModel, response_model_by_alias=False)
async def update_car_by_id(request: Request, id: str, user = Depends(auth_handler.auth_wrapper), car: UpdateCarModel = Body(...)):
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Car with {id} not found")

    car = {
        k: v
        for k, v in car.model_dump(by_alias=True).items() if v is not None and k != "_id"
    }

    if len(car) >= 1:
        cars = request.app.db["cars"]
        update_result = await cars.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": car},
            return_document=ReturnDocument.AFTER,
        )

        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Car {id} not found")
    else:
        if (existing_car := await cars.find_one({"_id": id})) is not None:
            return existing_car
        else:
            raise HTTPException(status_code=404, detail=f"Car {id} not found")

@router.delete("/{id}", response_description="Delete existing car", response_model=CarModel, response_model_by_alias=False)
async def delete_car_by_id(request: Request, id: str, user = Depends(auth_handler.auth_wrapper)):
    cars = request.app.db["cars"]
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Car with {id} not found")

    delete_result = await cars.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Car with {id} not found")


