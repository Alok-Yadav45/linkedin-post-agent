from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import PostCreate, PostOut
from app.services.post_service import create_post_flow, publish_existing_post
from app.services.trending_service import generate_trending_posts


router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.post("/generate", response_model=PostOut)
async def generate_post(payload: PostCreate):
    try:
        post = await create_post_flow(
            payload.topic,
            payload.post_length,
            payload.auto_post
        )
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/publish/{post_id}")
async def publish_post(post_id: int):
    try:
        success = await publish_existing_post(post_id)
        if success:
            return {"success": True, "message": "Post published successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to publish")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/generate-trending")
async def generate_trending_posts_endpoint(auto_post: bool = False):
    try:
        result = await generate_trending_posts(max_topics=5, auto_post=auto_post)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))