from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from infrastructure.fastapi_cfg.lifespan import lifespan
from infrastructure.fastapi_cfg.rate_limiter import limiter

app = FastAPI(debug=True, lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
