from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

def create(db: Session, resource: schemas.ResourceCreate):
    # Create a new instance of the Resource model with the provided data
    db_resource = models.Resource(
        name=resource.name,
        type=resource.type,
        quantity=resource.quantity
    )
    # Add the newly created Resource object to the database session
    db.add(db_resource)
    # Commit the changes to the database
    db.commit()
    # Refresh the Resource object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Return the newly created Resource object
    return db_resource

def read_all(db: Session):
    # Query the database to retrieve all resources
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id: int):
    # Query the database for the specific resource by its ID
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    # Raise an HTTP 404 error if the resource is not found
    if resource is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource

def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    # Query the database for the specific resource to update
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Check if the resource exists
    if db_resource.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    # Extract the update data from the provided 'resource' object
    update_data = resource.dict(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resource.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated resource record
    return db_resource.first()

def delete(db: Session, resource_id: int):
    # Query the database for the specific resource to delete
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Check if the resource exists
    if db_resource.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    # Delete the database record without synchronizing the session
    db_resource.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
