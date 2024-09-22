from fastapi import APIRouter, Depends, HTTPException, Response

from app.bookings.dao import BookingDao
from app.users.auth import authencicate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
  prefix="/auth",
  tags=["Auth and del"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
  existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
  if existing_user:
    raise HTTPException(status_code=500)
  hashed_password = get_password_hash(user_data.password)
  await UsersDAO.add(email=user_data.email, hashed_password = hashed_password)

@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
  user = await authencicate_user(user_data.email, user_data.password)
  if not user:
    raise HTTPException(status_code=401)
  access_token = create_access_token({"sub":str(user.id)})
  response.set_cookie("booking_access_token", access_token, httponly=True, secure=True)


@router.post("/logout")
async def logout(response: Response, user: Users = Depends(get_current_user)):
  try:
    response.delete_cookie("booking_access_token")
    return f"You logout sucsesful"
  except:
    raise HTTPException(status_code=400)


@router.delete("/delete_account")
async def delete(user: Users=Depends(get_current_user)):
  return await UsersDAO.delete_user(user_id=user.id)
