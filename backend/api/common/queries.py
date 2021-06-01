

class UserQ:
    BY_USERNAME = "SELECT * FROM users WHERE username=$1"
    BY_EMAIL = "SELECT email FROM users WHERE email=$1"
    BY_EMAIL_OR_USERNAME = "SELECT email, username FROM users WHERE email = $1 OR username = $2"
    
class AccountQ:
    NEW = """
        WITH ins1 AS (
        INSERT INTO users(username, email, password)
        VALUES($1, $2, $3) 
        RETURNING *
    ), ins2 AS (
            INSERT INTO user_profiles(uid, display_name, color)
            VALUES((select uid from ins1), $4, $5)
            RETURNING *
        )
    SELECT ins1.username, ins1.uid
    from ins1 join ins2 on ins1.uid = ins2.uid;
    """