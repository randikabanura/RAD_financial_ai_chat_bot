import openai
import gradio as gr
import random
import time

openai.api_key = "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"

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]
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
        bot_message = chatbot_response(message)
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()
