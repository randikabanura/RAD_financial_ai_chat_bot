import openai
import gradio as gr
import time
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

messages = [
    {"role": "system",
     "content": "You are an AI specialized in Financial Advice  in context of Sri Lankan investment and"
                "wealth generation options. Do not answer anything other than Financial Advice"
                "queries."},
]

questions = {
    "Please refer the language you wish to continue?": None,
    "Are you comfortable with higher-risk investments for potentially higher returns, or do you prefer lower-risk "
    "options?": None,
    "Are you aiming for long-term wealth accumulation, retirement planning, or specific short-term objectives?": None
}

initial_message = "Hello! I'm here to support you for investment and financial decision making. I am an  AI " \
                  "specialized in Financial Advice  in context of Sri Lankan investment and wealth generation options. "


def chatbot_response(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


with gr.Blocks() as demo:
    gr.Markdown("""# Financial ChatBot""")

    chatbot = gr.Chatbot(value=[[None, initial_message], [None, list(questions.keys())[0]]], height=600)
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        for item in questions.keys():
            if questions[item] is None:
                questions[item] = message
                break

        for item in questions.keys():
            if questions[item] is None:
                chat_history.append((message, item))
                time.sleep(2)
                return "", chat_history

        bot_message = chatbot_response(message)
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot], scroll_to_output=True)

if __name__ == "__main__":
    demo.launch()
