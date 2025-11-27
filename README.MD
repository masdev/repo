chapter7 % source ./venv7/bin/activate

#model_config = ConfigDict (extra="forbid", populate_by_name=True) 
#to have a possibility to address MongoDB _id with the alias name id in our model

class CarModel(BaseModel):
    .....
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        populate_by_alias=True,
        arbitrary_types_allowed=True,
        .....


Check and update if needed launch.json for debugger
.../.vscode/launch.json

chapter7 % pip3 install cloudinary python-multipart