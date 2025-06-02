# Standard library import
import logging
import requests

# Third-party imports
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.getenv('TWILIO_NUMBER')

hf_token = os.getenv("HF_TOKEN")
hf_model = os.getenv("HF_MODEL")
hf_url = f"https://router.huggingface.co/hf-inference/models/{hf_model}/v1/chat/completions"
headers = {"Authorization": f"Bearer {hf_token}"}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_huggingface(prompt: str) -> str:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "model": hf_model,
    }
    try:
        response = requests.post(hf_url, headers=headers, json=payload)
        response.raise_for_status()
        generated = response.json()

        try:
            result_text = generated["choices"][0]["message"]["content"]
        except Exception as e:
            result_text = f"Could not parse the HF response: {e}"
    except Exception as e:
        result_text = f"HF API error: {e}"

    return result_text


# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")