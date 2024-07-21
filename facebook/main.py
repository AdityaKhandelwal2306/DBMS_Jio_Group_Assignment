from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import FaissIndex
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index = FaissIndex(dimension=384)

class Vector(BaseModel):
    text: str

@app.post("/vectors/")
async def api_add_vector(vector: Vector):
    embedding = model.encode([vector.text])[0]
    id=index.create(embedding)
    return {"message": "Vector added successfully","id":id}

@app.get("/vectors/search/{id}")
async def api_search_vector(id: int):
    embedding = index.read(id)
    if embedding is None:
        raise HTTPException(status_code=404, detail="Vector not found")
    return {"embedding": embedding.tolist()}

@app.put("/vectors/update/{vector_id}")
async def api_update_vector(vector_id: int, text: str):
    embedding = model.encode([text])[0]
    success = index.update(vector_id, embedding)
    if not success:
        raise HTTPException(status_code=404, detail="Vector not found")
    return {"message": "Vector updated successfully"}

@app.delete("/vectors/delete/{vector_id}")
async def api_delete_vector(vector_id: int):
    success=index.delete(vector_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vector not found")
    return {"message": "Vector deleted successfully"}
