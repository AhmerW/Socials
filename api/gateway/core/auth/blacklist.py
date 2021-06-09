class TestUser:
    username = 'test'

BLACKLISTED_USERNAMES = (
    TestUser.username,
    'admin',
    'owner'
)

def approveUsername(username):
    return username in BLACKLISTED_USERNAMES