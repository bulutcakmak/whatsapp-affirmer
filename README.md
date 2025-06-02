# Whatsapp Affirmer

## v4.0

Not everyone has locally installed AI, so let's decrease the dependencies a bit. Our chat bot can now rely on Hugging Face to generate its responses! As of June 2, 2025, one can use a free tier account for costs up to $0.10 which should on smaller models be plenty. The cost can be maintained by putting a limit on max tokens or instructing the model to generate "short" responses. At the moment, we do store all messages on Postgres, but the model is not instructed to maintain conversation history. That is, the current bot will be able to answer one-time questions and not recall context. 

## v3.0

We now truly have AI functionality! OpenAI has no free-tier API interface, so I opted for a local language model using Ollama. Now, in addition to uvicorn and ngrok, you also need to locally run your favorite LLM by executing `ollama run mistral` on terminal. The model being used, along with the URL it will be run on, should be defined in the `.env` file. Also, the default behavior of the bot is now to send the LLM-generated response to the number that texted the bot. Note the assumption that we are using WhatsApp exclusively.

## v2.0

The slightly more complex version that stores all conversations in a PostgreSQL database. `app.py` remains in the repository for reference to MVP, but this version uses uvicorn to execute `main.py` and run up an active Twilio service. `example-env.txt` needs to be copied to `.env` and filled per implementation. 99% inspired by the Twilio blog post at https://www.twilio.com/en-us/blog/ai-chatbot-whatsapp-python-twilio-openai except I use `dotenv` and `os` instead of `decouple` to access the environment variables.

## MVP

The basic version that will run a server for the bot to run on. Requires `flask`, `twilio`, and also `ngrok` to configure a webhook at Twilio.

Assuming everything is set up, after running `python app.py` and `ngrok http 5001` (note: `5001` is the port used in the current script, could be changed to any number), you should be able to send messages to the accredited Twilio bot and receive the automatic response "yes cutie".