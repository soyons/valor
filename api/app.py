from fastapi import FastAPI
from auth import login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(login.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 允许来源列表，你可以指定具体的来源，如["http://localhost:8000", "http://yourdomain.com"]
    allow_credentials=True,  # 是否允许验证信息（如cookies或Authorization headers） 
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头部
)
