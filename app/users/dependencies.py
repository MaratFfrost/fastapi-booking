from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request
import jwt
from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
  token = request.cookies.get("booking_access_token")
  if not token:
    raise HTTPException(status_code=401)
  return token



async def get_current_user(token: str = Depends(get_token)):
  try:
    payload = jwt.decode(
      token, settings.KEY, settings.ALGORITM
    )
  except jwt.PyJWTError:
    raise HTTPException(status_code=401)
  expire: str = payload.get("exp")
  if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
    raise HTTPException(status_code=401)
  user_id = payload.get("sub")
  if not user_id:
    raise HTTPException(status_code=401)

  user = await UsersDAO.find_by_id(int(user_id))
  if not user:
    raise HTTPException(status_code=401)
  return user
