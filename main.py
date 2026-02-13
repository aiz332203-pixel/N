import os.path

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    # 这里可以添加更多允许的来源
    "http://localhost:5173/"
]
# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源,开发的时候可以使用*，企业上线时必须指定具体域名，以防止跨站攻击
    allow_credentials=True,# 允许携带cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            # 尝试获取请求的文件
            return await super().get_response(path, scope)
        except Exception:
            # 如果文件不存在，返回 index.html
            return FileResponse(os.path.join(self.directory, "index.html"))
#注册路由
app.include_router(news.router)
if os.path.exists("dist"):
    app.mount("/", SPAStaticFiles(directory="dist"), name="static")