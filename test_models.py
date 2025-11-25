from models import CarModel, CarCollection, UpdateCarModel

carModel1 = CarModel(brand="bMW", make="x6", year=2025, cm3=4000, km=1, price=100000)
print(carModel1.model_dump())

carModel2 = CarModel(brand="honda", make="centurion", year=2012, cm3=2000, km=10000, price=20000)
print(carModel2.model_dump())

carList = CarCollection(cars=[carModel1, carModel2])
print(carList.model_dump())

