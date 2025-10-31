from app.helpers.trending_topics import fetch_trending_topics
from app.services.post_service import create_post_flow

async def generate_trending_posts(max_topics: int = 5, auto_post: bool = False):
    """Fetch trending topics and generate LinkedIn posts for them."""
    trending = await fetch_trending_topics(max_items=max_topics)

    if not trending:
        return {"success": False, "message": "No trending topics found."}

    results = []
    for item in trending:
        topic = item["topic"]
        try:
            post = await create_post_flow(topic, length="short", auto_post=auto_post)
            results.append({
                "topic": topic,
                "post_id": post.id,
                "content": post.content,
                "auto_posted": post.posted == 1
            })
        except Exception as e:
            print(f"❌ Error generating post for '{topic}': {e}")

    return {"success": True, "count": len(results), "posts": results}

