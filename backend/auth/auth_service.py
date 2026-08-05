from sqlalchemy.orm import Session

from models.user import User

from schemas.user_register import UserRegister
from schemas.user_response import UserResponse

from auth.password import PasswordManager

from exceptions.auth_exception import AuthenticationError

from utils.logger import setup_logger


logger = setup_logger(__name__)


class AuthService:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def register(
        self,
        request: UserRegister
    ) -> UserResponse:

        logger.info(
            f"Registering user '{request.username}'."
        )

        # --------------------------
        # Check username
        # --------------------------

        existing_username = (

            self.db.query(User)

            .filter(
                User.username == request.username
            )

            .first()

        )

        if existing_username:

            raise AuthenticationError(
                "Username already exists."
            )

        # --------------------------
        # Check email
        # --------------------------

        existing_email = (

            self.db.query(User)

            .filter(
                User.email == request.email
            )

            .first()

        )

        if existing_email:

            raise AuthenticationError(
                "Email already exists."
            )

        # --------------------------
        # Hash password
        # --------------------------

        password_hash = (

            PasswordManager.hash_password(

                request.password

            )

        )

        # --------------------------
        # Create user
        # --------------------------

        user = User(

            username=request.username,

            email=request.email,

            password_hash=password_hash

        )

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        logger.info(
            f"User '{user.username}' registered successfully."
        )

        return UserResponse.model_validate(
            user
        )