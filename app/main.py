from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.auth import router as auth_router
from app.endpoints.career_path import router as career_path_router
from app.endpoints.chatbot import router as chatbot_router
from app.endpoints.college_bookmarks import router as college_bookmarks_router
from app.endpoints.college_comparison import router as college_comparison_router
from app.endpoints.college_reviews import router as college_reviews_router
from app.endpoints.college_search import router as college_search_router
from app.endpoints.recommendations import router as recommendations_router
from app.endpoints.scrape_gate_notifications import router as scrape_gate_notifications_router
from app.endpoints.scrape_nta_notifications import router as scrape_nta_notifications_router

app = FastAPI(
    title="College & Career Portal API",
    description="Backend API for college/career search, bookmarks, reviews, recommendations, chat, and notifications.",
    version="1.0.0"
)

# Set allowed origins for your frontend(s)
origins = [
    "http://localhost:3000",  # React dev server
    # Add production domains when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your endpoints here
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(career_path_router, prefix="/api", tags=["Career Path"])
app.include_router(chatbot_router, prefix="/api", tags=["Chatbot"])
app.include_router(college_bookmarks_router, prefix="/api", tags=["Bookmarks"])
app.include_router(college_comparison_router, prefix="/api", tags=["Comparison"])
app.include_router(college_reviews_router, prefix="/api", tags=["Reviews"])
app.include_router(college_search_router, prefix="/api", tags=["College Search"])
app.include_router(recommendations_router, prefix="/api", tags=["Recommendations"])
app.include_router(scrape_gate_notifications_router, prefix="/api", tags=["GATE Notifications"])
app.include_router(scrape_nta_notifications_router, prefix="/api", tags=["NTA Notifications"])

@app.get("/")
def root():
    return {"message": "Welcome to the College & Career Portal API!"}
