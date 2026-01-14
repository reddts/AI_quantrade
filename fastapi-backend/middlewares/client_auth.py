# middleware/client_auth.py

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.env import ClientConfig

# 示例：允许的客户端密钥列表（可从配置文件或数据库读取）
VALID_CLIENT_SECRETS = ClientConfig.client_secrets
path_whitelist = ClientConfig.get_path_whitelist()
suffix_whitelist = ClientConfig.get_suffix_whitelist()

class ClientSecretAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        path = request.url.path
        # 设置允许的 CORS 来源，可替换为实际域名
        allow_origin = request.headers.get("origin", "*")
        
        if any(path.startswith(p) for p in path_whitelist) or any(path.endswith(s) for s in suffix_whitelist):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = allow_origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response


        # 放行 OPTIONS 预检请求，不做校验，直接返回 200，并带上 CORS 头
        if request.method == "OPTIONS":
            headers = {
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "Authorization,Content-Type,X-Client-Secret"),
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400"  # 缓存预检结果，减少频率
            }
            return Response(status_code=200, headers=headers)
        
        # 从 Header 中提取客户端密钥
        client_secret = request.headers.get("X-Client-Secret")

        #加上控制台窗口提示VALID_CLIENT_SECRETS
        print("Valid client secrets:", VALID_CLIENT_SECRETS)

        # 校验客户端密钥是否有效
        if not client_secret or client_secret not in VALID_CLIENT_SECRETS:
             # 添加CORS头，避免浏览器跨域报错
            headers = {
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
            }

            print("client secret:", format(client_secret))
            return JSONResponse(
                status_code=401,
                content={"msg": "Unauthorized client. Invalid or missing client secret. Your Key IS:" + format(client_secret)},
                headers=headers
            )

        # 校验通过，继续请求
        response = await call_next(request)
        # 给所有正常响应加上 CORS 头
        response.headers["Access-Control-Allow-Origin"] = allow_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    
def add_client_auth_middleware(app):
    """
    添加客户端认证中间件

    :param app: FastAPI对象
    :return:
    """
    app.add_middleware(ClientSecretAuthMiddleware)

