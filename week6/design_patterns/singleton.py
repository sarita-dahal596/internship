from fastapi import FastAPI

app = FastAPI()


class Config:
    _instance = None

    def __new__(cls):

        # Create only one Config object
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


@app.get("/config")
def get_config():

    config1 = Config()
    config2 = Config()

    return {
        "same_object": config1 is config2
    }