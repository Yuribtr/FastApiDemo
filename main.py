from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get_index_page():
    return {'data': 'log list'}
