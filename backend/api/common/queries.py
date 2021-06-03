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
		kwargs = []
		for i, kw in enumerate(query):
			if ci is not None and cw is not None:
				if i+1 == len(query):
					# end
					kwargs.append(query[ci:i+1])
				elif not query[i].strip():
					kwargs.append(query[ci:i])
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
 		
		return (query, tuple(values))


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