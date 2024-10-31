from fastapi_cache import FastAPICache
from httpx import AsyncClient
import pytest

@pytest.fixture(autouse=True)
async def cleanup_redis():
    redis = FastAPICache.get_backend().redis
    yield
    await redis.flushdb()



@pytest.mark.parametrize("email,password,status_code", [
   ("user@example.com", "string", 200),
   ("user2@example.com", "hashedpassword2", 400),
   ("zklcjv", "s;dlkf", 422),
   ("", "", 422),
   ("", "sdfasdf", 422)
])
async def test_register_user(email,password,status_code, ac : AsyncClient):
   response = await ac.post("/auth/register", json={
      "email": email,
      "password": password
  })

   assert response.status_code == status_code


@pytest.mark.parametrize("email,code,status_code", [
   ("user@example.com", 456, 200),
   ("user1@example.com", 456, 400),
   ("", "", 404),
   ("user@example.com", 789, 404)
])
async def test_activate_account(email, code, status_code, ac: AsyncClient):
    redis = FastAPICache.get_backend().redis
    await redis.hset(f"verification:{code}", mapping={
        "email": email,
        "password": "password",
        "code": code
    })
    await redis.expire(f"verification:{code}", 15)

    response = await ac.post(f"/auth/activate_account?code={456}")
    assert response.status_code == status_code
