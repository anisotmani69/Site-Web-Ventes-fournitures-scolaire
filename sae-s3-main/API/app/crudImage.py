from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app import schemas, models

def get_imgae_by_name(image_name: str):
    return (f"../public/img/{image_name}.png")
