from fastapi.responses import JSONResponse

class Responses:
    REGISTRATION_COMPLTE = 'Your account has succesfully been registered at Socials.'
    REGISTRATION_PENDING = 'Please check your email in order to continue the registration process.'
    OTT_VERIFIED = 'OTToken successfully verified.'
    OTT_GENERATED = 'OTToken Successfully generated.'
    
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
        
    