from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MachineCreate(BaseModel):
    name: str
    muscle_group: str 
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

class WorkoutCreate(BaseModel):
    started_at: datetime
    notes: str | None = None


class MachineResponse(BaseModel):
    id: int
    name: str
    muscle_group: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)