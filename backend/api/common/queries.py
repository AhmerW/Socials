

class UserQ:
    BY_USERNAME = "select * from users where username=$1"
    VERIFY_EMAIL = "select email from users where email=$1"