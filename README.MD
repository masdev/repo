chapter7 % source ./venv7/bin/activate

#model_config = ConfigDict (extra="forbid", populate_by_name=True) 
# to have a possibility to address MongoDB _id with the alias name id in
# our model
class UserModel(BaseModel):
    id: int = Field(strict=True)
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field()
    password: str = Field(min_length=3, max_length=20, pattern="^[A-Za-z0-9]+$")
    model_config = ConfigDict (extra="forbid", populate_by_name=True)