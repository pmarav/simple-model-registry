from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import shutil
import psycopg2

DATABASE_NAME=os.getenv("DATABASE_NAME")
DATABASER_USER=os.getenv("DATABASER_USER")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE_HOST=os.getenv("DATABASE_HOST")

app = FastAPI()
UPLOAD_FOLDER = "models"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/models")
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    version: str = Form(...),
    accuracy: float = Form(...)
):
    if not file.filename.endswith(".pkl"):
        raise HTTPException(status_code=400, detail="Only .pkl files are allowed")
    
    filename = f"{name}_v{version}.pkl"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    connection = psycopg2.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASER_USER,
    password=DATABASE_PASSWORD
)
    cursor = connection.cursor()

    query = """
            INSERT INTO models (name, version, accuracy)
            VALUES (%s, %s, %s);
            """
    
    data = (name, version, accuracy)

    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()
    
    return {"message": "Model uploaded successfully", "model": {"name": name, "version": version, "accuracy": accuracy, "filepath": filepath}}

@app.get("/models")
def get_models():
    connection = psycopg2.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASER_USER,
    password=DATABASE_PASSWORD
    )

    cursor = connection.cursor()

    query = """
            SELECT row_to_json(models) FROM models;
            """
    
    cursor.execute(query)

    rows = cursor.fetchall()

    json_output = [row[0] for row in rows]

    print(json_output)
    print(type(json_output))
    cursor.close()
    connection.close()

    return json_output

@app.get("/models/{name}")
def get_model(name: str):
    connection = psycopg2.connect(
    host=DATABASE_HOST,
    database=DATABASE_NAME,
    user=DATABASER_USER,
    password=DATABASE_PASSWORD
    )

    cursor = connection.cursor()

    query = """
            SELECT row_to_json(models) FROM models WHERE name=%s;
            """
    
    cursor.execute(query, (name,))

    rows = cursor.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="Model not found")
    
    json_output = [row[0] for row in rows]

    print(json_output)
    print(type(json_output))
    cursor.close()
    connection.close()

    return json_output[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
