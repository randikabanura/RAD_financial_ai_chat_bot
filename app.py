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
                "wealth generation options."},
    {}
]

questions = {
    "Please refer the language you wish to continue?": None,
    "Are you comfortable with higher-risk investments for potentially higher returns, or do you prefer lower-risk "
    "options?": None,
    "Are you aiming for long-term wealth accumulation, retirement planning, or specific short-term objectives?": None,
    "How much capital do you have available for investment?": None,
    "Are you looking for a one time investment plan or a recursive investment plan?": None,
    "Are you looking for short-term gains or long-term investment opportunities?": None,
    "What is your current income level and financial stability?": None,
    "Do you have any existing debts or financial commitments that need to be considered?": None,
    "Are you interested in specific investment types such as real estate, stocks, bonds, mutual funds, or other "
    "options?": None,
    "Do you have any specific industries or sectors you want to focus on?": None,
    "What is your level of knowledge and experience in investment and finance?": None,
    "Have you invested before or are you a beginner seeking guidance?": None,
    "Are you interested in incorporating sustainability and social responsibility factors into your investment "
    "decisions?": None,
    "Do you prefer investing in companies that align with your values?": None,
    "Do you have any preferences regarding tax-efficient investment strategies?": None,
    "Do you have any preferences or concerns related to diversifying your investments?": None
}

initial_message = "Hello! I'm here to support you for investment and financial decision making.\nI am an AI " \
                  "specialized in Financial Advice in context of Sri Lankan investment and wealth generation options. "


def form_question():
    formed_question = "Generate a financial advice report in the context of Sri Lankan investment and wealth " \
                      "generation options, for given information as question and answer pairs. Report should consists " \
                      "of minimum of 1000 words and maximum 2000 words.\n"

    for key, value in questions.items():
        if value and value.strip():
            formed_question = formed_question + "\n" + key + ": " + value

    print(formed_question)
    return formed_question


def initialize_questions():
    for key in questions.keys():
        questions[key] = None


def chatbot_response(input):
    if input:
        try:
            messages[1] = {"role": "user", "content": input}
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            reply = chat.choices[0].message.content

            initialize_questions()
            return reply
        except Exception as e:
            print(e)
            return "Something went wrong!"


with gr.Blocks() as demo:
    gr.Markdown("""# Financial ChatBot""")

    chatbot = gr.Chatbot(value=[[None, initial_message], [None, list(questions.keys())[0]]], height=600)
    msg = gr.Textbox()
    btn = gr.Button(value="Clear")

    def respond(message, chat_history):
        for item in questions.keys():
            if questions[item] is None:
                questions[item] = message
                break

        for item in questions.keys():
            if questions[item] is None:
                chat_history.append((message, item))
                time.sleep(1)
                return "", chat_history

        processed_message = form_question()
        bot_message = chatbot_response(processed_message)
        chat_history.append((message, bot_message))
        chat_history.append((None, initial_message))
        chat_history.append((None, list(questions.keys())[0]))
        return "", chat_history

    def clear_chatbot(message, chat_history):
        chat_history.clear()
        chat_history.append((None, initial_message))
        chat_history.append((None, list(questions.keys())[0]))
        return "", chat_history

    btn.click(clear_chatbot, inputs=[msg, chatbot], outputs=[msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot], scroll_to_output=True)

if __name__ == "__main__":
    demo.launch()
