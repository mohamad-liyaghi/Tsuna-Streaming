from faker import Faker

faker = Faker()


def user_credentials(password: str = "1234PassWord") -> dict:
    """Return user credentials."""
    return {
        "email": faker.email(),
        "password": password,
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
    }
