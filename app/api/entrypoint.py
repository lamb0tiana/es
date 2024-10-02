from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn  # Import de uvicorn
from app.model.Contact import UserModel
from app.lib.mysql.DBclient import DBclient
import os
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/contact/edit/{contact_id}")
def edit_contact(contact_id: int, user: UserModel):
    load_dotenv()
    db = os.getenv('DB_NAME')
    # dbClient = DBclient(db)
    DBclient.update_contact(contact_id, user)
    return {"contact_id": contact_id}

if __name__ == "__main__":
    uvicorn.run("entrypoint:app", host="0.0.0.0", port=8000, reload=True)