import aiohttp
import feedparser
from bs4 import BeautifulSoup

TRENDING_NEWS_RSS = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"

async def fetch_trending_topics(max_items: int = 10):
    """Fetch trending topics from Google News RSS feed."""
    topics = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(TRENDING_NEWS_RSS, timeout=10) as response:
                content = await response.text()

        feed = feedparser.parse(content)

        for entry in feed.entries[:max_items]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            if title:
                topics.append({"topic": title, "link": link})

        return topics
    except Exception as e:
        print(f"⚠️ Error fetching trending topics: {e}")
        return []
