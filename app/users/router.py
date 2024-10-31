from fastapi import APIRouter, Depends, HTTPException, Response

import random

from fastapi_cache import FastAPICache


from app.tasks.tasks import send_email
from app.users.auth import authencicate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserLogin

router = APIRouter(
  prefix="/auth",
  tags=["Auth and del"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    verification_code = random.randint(100000, 999999)

    redis = FastAPICache.get_backend().redis
    await redis.hset(f"verification:{verification_code}", mapping ={
        "email": user_data.email,
        "password": user_data.password,
        "code": verification_code
    })
    await redis.expire(f"verification:{verification_code}", 600)
    send_email(verification_code, user_data.email)




@router.post("/activate_account")
async def activate_account(code: int):
    redis = FastAPICache.get_backend().redis

    user_data_from_cache = await redis.hgetall(f"verification:{code}")

    await redis.delete(f"verification:{code}")

    if not user_data_from_cache:
        raise HTTPException(status_code=404, detail="Verification data not found or expired.")
    data = [dict(user_data_from_cache)[i] for i in dict(user_data_from_cache)]

    existing_user = await UsersDAO.find_one_or_none(email=data[0].decode('utf-8'))

    if existing_user:
      raise HTTPException(status_code=400, detail="User already exists.")
    elif code == int(data[2]):
      hashed_password = get_password_hash(data[1])
      await UsersDAO.add(email=data[0].decode('utf-8'), hashed_password = hashed_password)
    else:
       raise HTTPException(status_code=418)




@router.post("/login")
async def login( response: Response, user_data: SUserLogin):
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
