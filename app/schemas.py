from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class MachineCreate(BaseModel):
    name: str
    muscle_group: str 
    description: str | None = None

class WorkoutCreate(BaseModel):
    started_at: datetime
    notes: str | None = None

class MachineUpdate(BaseModel):
    name: str | None = None
    muscle_group: str | None = None
    description: str | None = None

class MachineResponse(BaseModel):
    id: int
    name: str
    muscle_group: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)

class WorkoutCreate(BaseModel):
    started_at: datetime
    notes: str | None = None

class WorkoutFinish(BaseModel):
    ended_at: datetime 
    notes: str | None = None

class WorkoutResponse(BaseModel):
    id: int
    started_at: datetime
    ended_at: datetime | None
    notes: str | None

    model_config = ConfigDict(from_attributes=True)

class WorkoutActivityCreate(BaseModel):
    machine_id: int
    started_at: datetime

class WorkoutActivityResponse(BaseModel):
    id: int
    workout_id: int
    machine_id: int
    started_at: datetime
    ended_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class WorkoutActivityFinish(BaseModel):
    ended_at: datetime


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=320)
    password: str = Field(min_length=15, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

