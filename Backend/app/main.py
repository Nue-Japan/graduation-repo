from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Data-platform-backend-veta",version="1.0.0")

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://ar-dataplatform-veta.com",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Websocket route
# app.include_router(websocket_router, prefix="/ws",tags=["Websocket"])
# app.include_router(api_router, prefix="/api",tags=["API"])

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "backend is running"}

