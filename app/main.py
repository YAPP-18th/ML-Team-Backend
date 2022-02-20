import socketio
import uvicorn

from fastapi                        import FastAPI
from fastapi.middleware.cors        import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api                        import api_router
from app.core                       import (
                                        common_settings,
                                        develop_settings,
                                        deploy_settings
                                        )
from app.service                    import StudyNamespace

server  = FastAPI(title=common_settings.PROJECT_NAME)
sio     = socketio.AsyncServer(
    async_mode           = 'asgi',
    cors_allowed_origins = '*',
    debug                = True
)
sio.register_namespace(StudyNamespace(sio, '/study'))
sio_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=server)

server.add_middleware(
    CORSMiddleware,
    allow_origins     = deploy_settings.ALLOW_ORIGIN,
    allow_credentials = deploy_settings.ALLOW_CREDENTIAL,
    allow_methods     = deploy_settings.ALLOW_METHODS,
    allow_headers     = deploy_settings.ALLOW_HEADERS,
    expose_headers    = deploy_settings.ALLOW_EXPOSE_HEADERS
)
server.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts = deploy_settings.ALLOW_HOST,
)
server.add_websocket_route("/socket.io/", sio_app)
server.include_router(api_router, prefix=common_settings.COMMON_API)


if __name__ == "__main__":
    uvicorn.run(
        'app.main:server',
        host         = "0.0.0.0",
        port         = 8000,
        reload       = True,
        ssl_keyfile  = '/etc/letsencrypt/live/api.studeep.com/privkey.pem',
        ssl_certfile = '/etc/letsencrypt/live/api.studeep.com/fullchain.pem'
    )
