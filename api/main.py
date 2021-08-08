from gateway.server import app


app = app

if __name__ == "__main__":
    import uvicorn
    from common.settings import DEV_SETTINGS

    assert DEV_SETTINGS.IP.is_private

    uvicorn.run(
        "main:app", host=str(DEV_SETTINGS.IP), port=DEV_SETTINGS.PORT, reload=True
    )
