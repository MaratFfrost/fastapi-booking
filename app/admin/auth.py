from datetime import datetime, timezone
from app.config import settings
import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi import Depends, HTTPException, status
from starlette.responses import RedirectResponse

from fastapi_cache import FastAPICache

from app.admin.dao import AdminDao
from app.users.auth import create_access_token



class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        admin = await AdminDao.find_one_or_none(email=email, hashed_password=password)



        if not admin:
          return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

        redis = FastAPICache.get_backend().redis
        await redis.hset(f"current_admin:{admin.name}", mapping ={
          "email": admin.email
        })
        await redis.expire(f"current_admin:{admin.name}", 600)

        access_token = create_access_token({"sub": str(admin.id)})
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    @staticmethod
    def get_token(request: Request) -> str:
      token = request.cookies.get("session") or request.session.get("token")
      if not token:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
      return token

    async def get_current_admin(self, token: str = Depends(get_token)):
      try:
          payload = jwt.decode(token, settings.KEY, settings.ALGORITM)
      except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

      expire = payload.get("exp")
      if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

      admin_id = payload.get("sub")
      if not admin_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")

      admin = await AdminDao.find_by_id(int(admin_id))
      if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

      return admin

    async def authenticate(self, request: Request) -> bool:
      token = request.session.get("token")

      if not token:
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

      try:
        await self.get_current_admin(token)
      except HTTPException:
        return RedirectResponse(request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

      return True

authentication_backend = AdminAuth(secret_key="...")
