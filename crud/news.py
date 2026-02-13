# 新闻分类的封装crud操作
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    #模拟获取新闻分类列表-》先定义模型类,封装再实现crud操作
    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one() #只能有一个
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
async def add_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views + 1)
    result=await db.execute(stmt)
    await db.commit()
    #更新-》检查数据库是否真的命中了数据-》命中了返回True
    return result.rowcount > 0 if hasattr(result,'rowcount') else True
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit: int= 5):
    stmt=select(News).where(News.category_id==category_id,News.id != news_id).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()
