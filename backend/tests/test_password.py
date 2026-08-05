from backend.auth.password import PasswordManager

password = "Admin@123"

hashed = PasswordManager.hash_password(
    password
)

print(hashed)

print(
    PasswordManager.verify_password(
        password,
        hashed
    )
)

print(
    PasswordManager.verify_password(
        "WrongPassword",
        hashed
    )
)