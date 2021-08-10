from gateway.data.db.queries import Query, QueryCreator


class AccountQ(metaclass=QueryCreator):

    NEW = """
        WITH ins1 AS
        (
                    insert INTO users
                                (
                                            username,
                                            email,
                                            password,
                                            verified
                                )
                                VALUES
                                (
                                            {username},
                                            {email},
                                            {password},
                                            {verified}
                                )
                    returning   * ), ins2 AS
        (
                    INSERT INTO user_profiles
                                (
                                            UID,
                                            display_name
                                )
                                VALUES
                                (
                                (
                                    SELECT UID
                                    FROM   ins1
                                )
                                ,
                                {display_name}
                                )
                    returning   * )
        SELECT ins1.username,
            ins1.UID
        FROM   ins1
        join   ins2
        ON     ins1.UID = ins2.UID; 
    """
