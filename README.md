# Whatsapp Affirmer

## v2.0

The slightly more complex version that stores all conversations in a PostgreSQL database. `app.py` remains in the repository for reference to MVP, but this version uses uvicorn to execute `main.py` and run up an active Twilio service. `example-env.txt` needs to be copied to `.env` and filled per implementation. 99% inspired by the Twilio blog post at https://www.twilio.com/en-us/blog/ai-chatbot-whatsapp-python-twilio-openai except I use `dotenv` and `os` instead of `decouple` to access the environment variables.

## MVP

The basic version that will run a server for the bot to run on. Requires `flask`, `twilio`, and also `ngrok` to configure a webhook at Twilio.

Assuming everything is set up, after running `python app.py` and `ngrok http 5001` (note: `5001` is the port used in the current script, could be changed to any number), you should be able to send messages to the accredited Twilio bot and receive the automatic response "yes cutie".