# Whatsapp Affirmer

## MVP

The basic version that will run a server for the bot to run on. Requires `flask`, `twilio`, and also `ngrok` to configure a webhook at Twilio.

Assuming everything is set up, after running `python app.py` and `ngrok http 5001` (note: `5001` is the port used in the current script, could be changed to any number), you should be able to send messages to the accredited Twilio bot and receive the automatic response "yes cutie". 