from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings

# Create async engine for PostgreSQL
# Note: Special configuration for Supabase Session Pooler (pgbouncer in transaction mode)
# - statement_cache_size=0: Disables prepared statement caching in asyncpg
# - poolclass=NullPool: Disables SQLAlchemy connection pooling (pgbouncer handles this)
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
    poolclass=NullPool,
    connect_args={
        "statement_cache_size": 0,
        "server_settings": {"jit": "off"}
    }
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db():
    """Dependency to get database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            # Import models here so they register with Base.metadata
            from app.models import employee, attendance
            await conn.run_sync(Base.metadata.create_all)
        print(f"✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
        print(f"⚠️  Please check your DATABASE_URL in .env file")
        print(f"⚠️  Make sure you're using the Session Pooler (port 6543) from Supabase")


async def close_db():
    """Close database connection."""
    await engine.dispose()
    print("Database connection closed")
