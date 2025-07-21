"""Service for managing API keys."""

from sqlalchemy.orm import Session

from app.schemas.key import Key, KeyCreate, KeyUpdate


class KeyService:
    """Service for managing API keys."""

    def __init__(self, session: Session, project_id: str | None = None) -> None:
        """Initialize the key service with a database session."""
        self.session = session
        self.project_id = project_id

    def create(self, key_data: KeyCreate) -> Key:
        """Create a new key."""
        db_key = Key.model_validate(key_data)
        self.session.add(db_key)
        self.session.commit()
        self.session.refresh(db_key)
        return db_key

    def get_by_id(self, key_id: int) -> Key | None:
        """Get a key by ID."""
        return self.session.get(Key, key_id)

    def is_key_in_project(self, key_id: int, project_id: int) -> bool:
        """Check if a key belongs to the given project."""
        db_key = self.get_by_id(key_id)
        return db_key is not None and db_key.project_id == project_id

    def get_by_value(self, key_value: str) -> Key | None:
        """Get a key by its value."""
        return self.session.query(Key).filter(Key.key == key_value).first()

    def list_(
        self,
        skip: int = 0,
        limit: int = 100,
        *,
        show_inactive: bool = False,
    ) -> list[Key]:
        """Get all keys with pagination."""
        query = self.session.query(Key)
        if self.project_id:
            query = query.filter(Key.project_id == self.project_id)
        if not show_inactive:
            query = query.filter(Key.is_active)
        query = query.offset(skip).limit(limit)
        return query.all()

    def update(self, key_id: int, key_data: KeyUpdate) -> Key | None:
        """Update an existing key."""
        db_key = self.get_by_id(key_id)
        if not db_key:
            return None
        update_data = key_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_key, field, value)

        self.session.commit()
        self.session.refresh(db_key)
        return db_key

    def delete(self, key_id: int) -> bool:
        """Delete a key."""
        db_key = self.get_by_id(key_id)
        if not db_key:
            return False
        self.session.delete(db_key)
        self.session.commit()
        return True
