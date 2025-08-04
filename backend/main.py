from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.llm_memory import router as llm_router

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(llm_router)

@app.get("/")
def read_root():
    return {"msg": "🔥 Dardy Empire API running"}
