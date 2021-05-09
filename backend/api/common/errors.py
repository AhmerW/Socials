
class Errors:
    invalid_arguments = 0
    invalid_data = 1
    channel_not_found = 2
    
    @classmethod
    def json(cls, error):
        return {'error': str(error), 'error_code': error.value}