from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from infrastructure.environment import env
from infrastructure.fastapi_cfg.lifespan import lifespan
from infrastructure.fastapi_cfg.rate_limiter import limiter

app = FastAPI(debug=env.debug, lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
