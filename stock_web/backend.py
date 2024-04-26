from fastapi import FastAPI, Form, Request, HTTPException
import httpx 
import os
from pydantic import BaseModel
from uvicorn import Config, Server
from discord import Bot
from bot import broadcast_buy, broadcast_sell

from bot import bot
from config import API_HOST, API_PORT, MAIN_CHANNEL, STCOK_CHANNEL
from config import LOGIN_CLIENT_ID, LOGIN_CLIENT_SECRET, LOGIN_REDIRCET_URL

app = FastAPI()

DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/users/@me"

class BuyOrder(BaseModel):
    stock_code: str  # 添加股票代碼字段
    stock_name: str
    stock_amount: int
    stock_price: float

@app.post("/submit-buy-order")
async def submit_buy_order(
    stock_code: str = Form(),
    stock_name: str = Form(),
    stock_amount: int = Form(),
    stock_price: float = Form(),
):

    print(f"股票名稱：{stock_name} 股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}")
    await broadcast_buy(stock_name=stock_name,stock_code=stock_code,stock_amount=stock_amount,stock_price=stock_price)
    return {"OK"}
@app.post("/submit-sell-order")
async def submit_sell_order (
    stock_code: str = Form(),
    stock_name: str = Form(),
    stock_amount: int = Form(),
    stock_price: float = Form(),
):
    print(f"股票名稱：{stock_name} 股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}")
    await broadcast_sell(stock_name=stock_name,stock_code=stock_code,stock_amount=stock_amount,stock_price=stock_price)
    return {"OK"} 

@app.post("/auth/callback")
async def auth_callback(request: Request):
    form_data = await request.form()
    access_code = form_data.get("code")
    token_data = {
        "client_id": LOGIN_CLIENT_ID,
        "client_secret": LOGIN_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": access_code,
        "redirect_uri": LOGIN_REDIRCET_URL
    }
    async with httpx.AsyncClient() as client:
        token_response = await client.post(DISCORD_TOKEN_URL, data=token_data)
        token_response_json = token_response.json()
        access_token = token_response_json.get("access_token")
        
        # 使用 access token 獲取用戶資訊
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_response = await client.get(DISCORD_API_URL, headers=headers)
        user_data = user_response.json()
        return user_data

async def start_api():
    config = Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
    )
    server = Server(config=config)

    await server.serve()

