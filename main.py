# Third-party imports
from fastapi import FastAPI, Form, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Internal imports
from models import Conversation, SessionLocal
from utils import query_huggingface, send_message, logger

# Initialize FastAPI app
app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/message")
async def reply(Body: str = Form(), From: str = Form(), db: Session = Depends(get_db)):

    sender_to = From.replace("whatsapp:", "")

    # Store the conversation in the database
    try:
        # The generated text

        # chat_response = query_huggingface(f"User: {Body}\nBot:")
        chat_response = query_huggingface(Body)
        
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
    except Exception as e:
        db.rollback()
        logger.error(f"Unidentified Error: {e}")
        chat_response = "Sorry, something went wrong generating a response."

    send_message(sender_to, chat_response)
    return ""
