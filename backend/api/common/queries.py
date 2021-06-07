class Query():
	def __init__(self, query, format_chr = '$'):
		self._q = query
		self._fc = format_chr

	@property
	def query(self):
		return self._q

	def __repr__(self):
		return self._q

	def __call__(self, **kwargs):
		return self.format(**kwargs)
		

	def _getKwargs(self):
		"""Extracts each keyword argument from the query"""
		ci = None
		cw = None
		kwargs = list()
		for i, kw in enumerate(self._q):
			if ci is not None and cw is not None:
				if i+1 == len(self._q):
					# end
					kwargs.append(self._q[ci:i+1])
				elif not self._q[i].strip() or self._q[i] in (',', ')', '('):
					kwargs.append(self._q[ci:i])
					ci, cw = None, None
			if kw.startswith(self._fc):
				ci, cw = i, kw

		return kwargs

	def format(self, **kwargs):
		"""
		**kwargs
			- List of keyword arguments to apply to the query

		returns:
			(str, tuple)
			which represents the query and the values applied to each kwarg.

		"""

		kwargs_extracted =  self._getKwargs()
		kwargs_no_fc = [kw[1::] for kw in kwargs_extracted]

		kwargs_sorted = sorted(kwargs, key = kwargs_no_fc.index)
		values = [kwargs.get(k) for k in kwargs_sorted]

		query = self._q
		used = list()
		c  = 0

		# Replace each keyword argument with an appropiate index number
		for i, kw in enumerate(kwargs_extracted):
			kwe = kw[1::]
			if not kwe in used:
				used.append(kwe)
				c += 1
			query = query.replace(kw, f'{self._fc}{c}')
 		
		return (query, *values)


class _QueryCreator(type):
    def __getattribute__(self, name) -> Query:
        return Query(
            object.__getattribute__(self, name),
            format_chr = '$'
        )


class UserQ(metaclass = _QueryCreator):
    FROM_USERNAME = "SELECT * FROM users WHERE username=$username"
    FROM_EMAIL = "SELECT email FROM users WHERE email=$email"
    FROM_USERNAME_OR_EMAIL = "SELECT email, username FROM users WHERE email = $email OR username = $username"
    
class AccountQ(metaclass = _QueryCreator):

    NEW = """
        WITH ins1 AS (
        INSERT INTO users(username, email, password, verified)
        VALUES($username, $email, $password, $verified) 
        RETURNING *
    ), ins2 AS (
            INSERT INTO user_profiles(uid, display_name)
            VALUES((select uid from ins1), $display_name)
            RETURNING *
        )
    SELECT ins1.username, ins1.uid
    from ins1 join ins2 on ins1.uid = ins2.uid;
    """