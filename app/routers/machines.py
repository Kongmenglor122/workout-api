from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select


from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/machines",
    tags=["Machines"],
)

@router.post("", status_code=201, response_model=schemas.MachineResponse)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db),):
    new_machine = models.Machine(name = machine.name, muscle_group = machine.muscle_group, description = machine.description)

    db.add(new_machine) # 	Register the object with the session for insertion
    db.commit() # Flush pending changes to PostgreSQL and commit the transaction
    db.refresh(new_machine) # Reload the saved record, including its generated ID

    return new_machine # Return the machine from the endpoint

@router.get("", response_model=list[schemas.MachineResponse])
def get_all_machines(db: Session = Depends(get_db),):
    statement = select(models.Machine).order_by(models.Machine.id)
    machines = db.scalars(statement).all()

    return machines
@router.get("/{id}", response_model=schemas.MachineResponse)
def get_machine_by_id(id: int, db: Session = Depends(get_db),):
    machine = db.get(models.Machine, id)

    if machine == None:
        raise HTTPException(status_code=404, detail="Machine not found")

    return machine
@router.delete("/{id}", status_code=204)
def delete_machine(id: int, db: Session = Depends(get_db)):
    machine = db.get(models.Machine, id)

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )
    db.delete(machine)
    print(db.delete(machine))
    db.commit()
    return Response(status_code=204)
@router.patch("/{id}", response_model=schemas.MachineResponse)
def update_machine_by_id(id:int, updates: schemas.MachineUpdate,db: Session = Depends(get_db)):

    machine = db.get(models.Machine, id)

    if machine is None:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )
    
    update_values = updates.model_dump(exclude_unset=True)
    for field in ("name", "muscle_group", "description"):
        if field in update_values and update_values[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )
    for field, value in update_values.items():
        setattr(machine, field, value)

    db.commit()
    db.refresh(machine)

    return machine