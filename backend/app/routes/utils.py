from fastapi import HTTPException


def not_found(name: str):
    raise HTTPException(status_code=404, detail=f"{name} no encontrado")
