import uvicorn
import dotenv

from app_factory import app_factory

dotenv.load_dotenv()
app = app_factory()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
