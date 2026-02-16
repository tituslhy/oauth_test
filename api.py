import os
from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

_ = load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("CHAINLIT_AUTH_SECRET"))
oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("OAUTH_GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {"scope": "openid email profile"}
)

@app.get("/")
async def home():
    return HTMLResponse('<a href="/login">Login with Google</a>')

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")
    return {
        "status": "success",
        "message": f"Hello {user['given_name']} {user['family_name']}!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)