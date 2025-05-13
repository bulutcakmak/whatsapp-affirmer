from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import datetime

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{time}] Message from {sender}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message("yes cutie")  # 💖 fixed response

    return str(resp)

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)
