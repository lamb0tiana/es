from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from app.model.Contact import ContactModel
from app.lib.mysql.DBclient import DBclient
from fastapi.responses import JSONResponse

import os

app = FastAPI(title="Contact",
              description="Contact",
              version="1.0.0", )


@app.put("/contact/edit/{contact_id}", responses={
    204: {"description": "successfull update"},
    200: {"description": "No record updated"},
})
def edit_contact(contact_id: int, user: ContactModel):
    load_dotenv()
    db = os.getenv('DB_NAME')
    dbClient = DBclient(db)
    if dbClient.update_contact(contact_id, user) > 0:
        return JSONResponse(status_code=204, content={"success": "true"})
    return {"message": "no record updated"}


if __name__ == "__main__":
    uvicorn.run("entrypoint:app", host="0.0.0.0", port=8000, reload=True)
