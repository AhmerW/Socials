from gateway.data.db.queries import Query, QueryCreator


class UserQ(metaclass=QueryCreator):
    FROM_USERNAME = "SELECT * FROM public.users WHERE username={username}"

    FROM_EMAIL = "SELECT email FROM public.users WHERE email={email}"
    FROM_USERNAME_OR_EMAIL = "SELECT email, username FROM public.users WHERE email = {email} OR username = {username}"
    EXISTS = "SELECT uid from public.users where uid={uid}"

    VERIFY = "UPDATE users SET verified=TRUE where uid={uid}"

    PROFILE_FROM_USERNAME = """
        SELECT 
        public.users.username,
        public.users.premium,
        public.users.uid,
        up.display_name,
        up.pfp
        from public.users
        JOIN public.user_profiles  as up
        ON public.users.uid = up.uid
        WHERE public.users.username = {username};
    """
    PROFILE_FROM_UID = """
        SELECT 
        public.users.username,
        public.users.premium,
        public.users.uid,
        up.display_name,
        up.pfp
        from public.users
        JOIN public.user_profiles  as up
        ON public.users.uid = up.uid
        WHERE public.users.uid = {uid};
    """

    TOTAL_CHATS = """
    SELECT COUNT(*) from chat.chat_members where chat.chat_members.chat_member_uid = {uid}
    """
