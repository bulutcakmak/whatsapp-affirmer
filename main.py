# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Depends
import httpx
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Standard libraries
import json
import os

# Internal imports
from models import Conversation, SessionLocal
from utils import send_message, logger

# Load environment variables
load_dotenv()
ollama_url = os.getenv("OLLAMA_URL")
ollama_model = os.getenv("OLLAMA_MODEL")

# Initialize FastAPI app
app = FastAPI()

async def generate_with_ollama(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(
                ollama_url,
                json={
                    "model": ollama_model,
                    "prompt": prompt,
                    "stream": False
                }
            )

            if response.status_code != 200:
                logger.error(f"Non-200 status: {response.status_code}")
                logger.error(f"Body: {response.text}")
                return "The model failed to respond."

            try:
                # Try manually parsing just in case
                raw = response.text.strip()
                data = json.loads(raw)
                return data.get("response", "").strip()
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON: {response.text}")
                return "Invalid response from model."

    except httpx.TimeoutException:
        logger.error("Timeout while waiting for model.")
        return "The model took too long to respond."


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/message")
async def reply(Body: str = Form(), From: str = Form(), db: Session = Depends(get_db)):

    # Store the conversation in the database
    try:
        # The generated text
        chat_response = await generate_with_ollama(Body)
        sender_to = From.replace("whatsapp:", "")
        
        conversation = Conversation(
            sender_from=From,
            sender_to=sender_to,
            message=Body,
            response=chat_response
            )
        db.add(conversation)
        db.commit()
        logger.info(f"Conversation #{conversation.id} stored in database")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
        chat_response = "Sorry, there was an error storing the conversation."
    except httpx.RequestError as e:
        db.rollback()
        logger.error(f"Request to Ollama failed: {e}")
        return "Sorry, I couldn't reach the model."
    except Exception as e:
        db.rollback()
        logger.error(f"Ollama Error: {e}")
        chat_response = "Sorry, something went wrong generating a response."

    send_message(sender_to, chat_response)
    return ""