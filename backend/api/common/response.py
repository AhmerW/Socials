from fastapi.responses import JSONResponse

class Responses:
    CODE_VERIFIED = 'Code successfully verified.'
    CODE_GENERATED = 'Code Successfully generated.'
    
def Success(detail, data = {}, status = 200):
    return JSONResponse(
        status_code = status,
        content = {
            'ok': True,
            'status': status,
            'error': {},
            'detail': detail,
            'data': data
        }
    )
        
    