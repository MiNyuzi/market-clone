from fastapi import FastAPI,UploadFile,Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder #js응답으로 바꿔준다?
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3 #dbeaver연결

con = sqlite3.connect('please.db', check_same_thread=False)
cur = con.cursor()


#테이블이 없을때만 생성되는 SQL문
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	          id INTEGER PRIMARY KEY, 
	          title TEXT NOT NULL, 
	          image BLOB, 
	          price INTEGER NOT NULL,
	          description TEXT,
              place TEXT NOT NULL,
	          insertAt INTEGER NOT NULL
            ); 
            """)

app = FastAPI()

@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str, Form()], 
                price:Annotated[int, Form()], 
                description:Annotated[str, Form()], 
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()]):
    #이미지 읽는 시간이 필요하다
    image_bytes = await image.read()
    # 변수 넣는 방법
    cur.execute(f"""
                INSERT INTO items(title, image, price, description, place, insertAt)
                VALUES ('{title}', '{image_bytes.hex()}' ,{price}, '{description}', '{place}',{ insertAt})
                """)
    con.commit()
    return '200'
    
@app.get('/items')
async def get_items():
    #컬럼명 가져오는 문법
    con.row_factory = sqlite3.Row 
    cur = con.cursor() #db를 가져오면서 커넥션의 현재위치를 cursor라고 표시하는데 ....
    rows =cur.execute(f"""
                      SELECT * from items;
                      """).fetchall() #가져오는 문법
    
    return JSONResponse(jsonable_encoder(dict(row) for row in rows)) #dict는 뭐라고요? rows가 어레이를 만들어주고 이렇게 쓰면 이쁘게 만들어준다

@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    #16진법
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id = {item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes)) #16진법을 바꾸게다

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")