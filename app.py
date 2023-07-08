import openai
import gradio as gr
import random
import time

openai.api_key = ""

messages = [
    {"role": "system", "content": "You are an AI specialized in Financial Advice  in context of Sri Lankan investment and"
                                  "wealth generation options. Do not answer anything other than food-related"
                                  "queries."},
]

questions = {
    "What is langauge you prefer ?": "",
    "Test": ""
}

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
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        for item in questions.items():
            chat_history.append((message, item.key))
            
        bot_message = chatbot_response(message)
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()
