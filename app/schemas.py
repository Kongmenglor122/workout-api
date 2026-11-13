from pydantic import BaseModel, ConfigDict
from datetime import datetime


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