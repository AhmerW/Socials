class TestUser:
    username = "test"


BLACKLISTED_USERNAMES = (
    TestUser.username,
    "admin",
    "owner",
)


def approveUsername(username) -> bool:
    return not username in BLACKLISTED_USERNAMES
