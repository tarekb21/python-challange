from app.models import User

# In-memory database: tenant_id -> list of users
db: dict[str, list[User]] = {}
