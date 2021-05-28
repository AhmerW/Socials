from common.create_app import createApp

class ServerContext:
    pool = None
    codes = {}
    
app = createApp(
    title = 'Socials',
    
    redoc_url = None
)