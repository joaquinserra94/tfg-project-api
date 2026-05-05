import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, require_admin
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
import app.services.user_service as user_service

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=UserResponse,
    summary="Registrar usuario",
    description="Crea un nuevo usuario en el sistema a partir de un correo electrónico y una contraseña.",
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = user_service.get_user_by_email(db, user.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        return user_service.create_user(db, user)

    except IntegrityError:
        logger.exception("Integrity error while creating user")
        raise HTTPException(status_code=400, detail="Email already registered")

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while creating user")
        raise HTTPException(status_code=500, detail="Internal error while creating user")


@router.post(
    "/login",
    summary="Autenticación de usuario",
    description="Permite a un usuario autenticarse y obtener un token de acceso.",
)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(
        db,
        user_credentials.email,
        user_credentials.password,
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario autenticado",
    description="Devuelve el usuario autenticado. El frontend lo usa tras el login para saber si tiene rol de administrador.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Lista todos los usuarios del sistema. Requiere permisos de administrador.",
)
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return db.query(User).all()


@router.patch(
    "/{user_id}/admin",
    response_model=UserResponse,
    summary="Cambiar rol administrador",
    description="Otorga o revoca el rol de administrador a un usuario. Requiere permisos de administrador.",
)
def toggle_admin(
    user_id: int,
    is_admin: bool,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    target = db.query(User).filter(User.id == user_id).first()

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    if not is_admin and target.id == admin.id:
        remaining_admins = (
            db.query(User)
            .filter(User.is_admin == True, User.id != admin.id)
            .count()
        )

        if remaining_admins == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes revocarte a ti mismo siendo el último admin.",
            )

    target.is_admin = is_admin
    db.commit()
    db.refresh(target)

    return target