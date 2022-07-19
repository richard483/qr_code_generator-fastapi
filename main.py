import secrets
import pyqrcode

from typing import List

from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse

class Data(BaseModel):
    name: str
    link: str

class Datas(BaseModel):
    data: List[Data]

app = FastAPI()

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "username")
    correct_password = secrets.compare_digest(credentials.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_current_user():
    return "Welcome to nephren's qr code generator API :D"

@app.get("/qr/{web}")
async def generateQr(web):
    s = web
    url = pyqrcode.create(s)
    url.png("{}.png".format("generated"), scale = 6)
    return FileResponse("{}.png".format("generated"))

@app.get("/data/")
async def generateQrCode(data: Data):
    s = data.link
    url = pyqrcode.create(s)
    url.png("{}.png".format("generatedQR"), scale = 6)
    return FileResponse(path="{}.png".format("generatedQR"), filename="{}.png".format(data.name), media_type='png')
    # return data.link


@app.get("/datas/")
async def generateQrCode(datas: Datas):
    # s = datas.link
    # url = pyqrcode.create(s)
    # url.png("{}.png".format("generatedQR"), scale = 6)
    # return FileResponse(path="{}.png".format("generatedQR"), filename="{}.png".format(datas.name), media_type='png')
    return datas.data[2].name