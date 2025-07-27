"""User service for managing user CRUD operations."""

from sqlmodel import Session, select

from app.models.user import User


class UserService:
    """Service class for managing user CRUD operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the user service with a database session.

        Args:
            session: SQLModel database session for operations

        """
        self.session = session

    # def create(self, user_data: UserCreate) -> User:
    #     """Create a new user in the database.

    #     Args:
    #         user_data: User creation data containing required fields

    #     Returns:
    #         User: The created user with generated timestamps

    #     Raises:
    #         Exception: If user creation fails or email already exists

    #     """
    #     # Convert UserCreate to User model for database storage
    #     db_user = User.model_validate(user_data)

    #     self.session.add(db_user)
    #     self.session.commit()
    #     self.session.refresh(db_user)

    #     return db_user

    def get_by_id(self, user_id: str) -> User | None:
        """Retrieve a user by their ID.

        Args:
            user_id: The unique identifier for the user

        Returns:
            User if found, None otherwise

        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address of the user

        Returns:
            User if found, None otherwise

        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    # def update(
    #     self,
    #     user_id: str,
    #     *,
    #     user: UserUpdate,
    # ) -> User | None:
    #     """Update a user's information.

    #     Args:
    #         user_id: The unique identifier for the user
    #         user: User update data containing fields to modify

    #     Returns:
    #         Updated User object if successful, None if user not found

    #     """
    #     db_user = self.get_by_id(user_id)
    #     if not db_user:
    #         return None

    #     # Update fields from UserUpdate model
    #     # Source: https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#update-the-hero-in-the-database
    #     user_data = user.model_dump(exclude_unset=True)
    #     db_user.sqlmodel_update(user_data)

    #     self.session.add(db_user)
    #     self.session.commit()
    #     self.session.refresh(db_user)

    #     return db_user

    def delete(self, user_id: str) -> bool:
        """Delete a user from the database.

        Args:
            user_id: The unique identifier for the user

        Returns:
            True if user was deleted, False if not found

        """
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()

        return True

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[User]:
        """List users with optional filtering and pagination.

        Args:
            limit: Maximum number of users to return (default: 100)
            offset: Number of users to skip (default: 0)

        Returns:
            List of User objects matching the criteria

        """
        return self.session.exec(select(User).offset(offset).limit(limit)).all()
