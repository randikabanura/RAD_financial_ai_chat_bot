import configparser
import openai
import gradio as gr
import time
import os
from dotenv import load_dotenv
from encryption_decryption import decrypt_value

load_dotenv()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = ""

messages = [
    {"role": "system",
     "content": "You are an AI specialized in Financial Advice  in context of Sri Lankan investment and"
                "wealth generation options."},
    {}
]

questions = {}

questions_english = {
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

questions_sinhala = {
    "ඔබගේ රුචිකත්වය ඉහළ අවදානම් සහිත ඉහළ ප්‍රතිලාභ සඳහාද නැතහොත් අඩු අවදානම් විකල්ප සඳහාද?": None,
    "ඔබ දිගුකාලීන ධනය ආයෝජන කිරීම, විශ්‍රාම සැලසුම් කිරීම හෝ විශේෂිත කෙටි කාලීන අරමුණු සඳහා ඉලක්ක කරන්නේද?": None,
    "ආයෝජනය සඳහා ඔබට කොපමණ ප්‍රාග්ධනයක් තිබේද?": None,
    "ඔබ සොයන්නේ එක් වර ආයෝජන සැලැස්මක් හෝ පුනරාවර්තන ආයෝජන සැලැස්මක් ද?": None,
    "ඔබ සොයන්නෙ කෙටි කාලීන ආයෝජන අවස්ථාද? නැත්නම් දිගු කාලීන ආයෝජන අවස්ථාද?": None,
    "ඔබගේ වර්තමාන ආදායම් මට්ටම සහ මූල්‍ය ස්ථාවරත්වය කුමක්ද?": None,
    "ඔබට සලකා බැලිය යුතු පවතින ණය හෝ මූල්‍ය බැඳීම් තිබේද?": None,
    "නිශ්චල දේපල, කොටස්, බැඳුම්කර, අන්‍යෝන්‍ය අරමුදල් හෝ වෙනත් විකල්ප වැනි විශේෂිත ආයෝජන වර්ග ගැන ඔබේ විශේෂ කැමැත්තක් "
    "තිබේද?": None,
    "ඔබට අවධානය යොමු කිරීමට අවශ්‍ය විශේෂිත කර්මාන්ත හෝ අංශ තිබේද?": None,
    "ආයෝජන සහ මුල්‍ය කටයුතු සම්බන්ධයෙන් ඔබගේ දැනුම සහ අත්දැකීම් මට්ටම කුමක්ද?": None,
    "ඔබ මීට පෙර ආයෝජනය කර තිබේද නැතහොත් ඔබ මග පෙන්වීමක් සොයන ආධුනිකයෙක්ද?": None,
    "ඔබේ ආයෝජන තීරණවලට තිරසාරත්වය සහ සමාජ වගකීම් සාධක ඇතුළත් කිරීමට ඔබ කැමතිද?": None,
    "ඔබ ඔබේ වටිනාකම් සමඟ ගැලපෙන සමාගම්වල ආයෝජනය කිරීමට කැමතිද?": None,
    "බදු-කාර්යක්ෂම ආයෝජන උපාය මාර්ග සම්බන්ධයෙන් ඔබට කිසියම් කැමැත්තක් තිබේද?": None,
    "ඔබේ ආයෝජන විවිධාංගීකරණය කිරීම සම්බන්ධයෙන් ඔබට කිසියම් කැමැත්තක් තිබේද?": None
}

initial_message_english = "Hello! I'm here to support you for investment and financial decision making.\nI am an AI " \
                  "specialized in Financial Advice in context of Sri Lankan investment and wealth generation options. "
initial_message_sinhala = "ආයුබෝවන්! ආයෝජන සහ මූල්‍ය තීරණ ගැනීම සඳහා ඔබට සහාය වීමට මම මෙහි සිටිමි. මම ශ්‍රී ලංකාවේ " \
                          "ආයෝජන සහ ධන උත්පාදන විකල්පයන් සම්බන්ධයෙන් මූල්‍ය උපදෙස් පිළිබඳ කෘත්‍ය බුද්ධි මෙවලමකි."

report_heading_english = "Financial Advice Report \n======================================"
report_heading_sinhala = "මූල්‍ය උපදෙස් වාර්තාව \n======================================"


language_input_var = None

questionnaire_english = gr.Chatbot(value=[[None, initial_message_english], [None, list(questions_english.keys())[0]]], height=600)
questionnaire_sinhala = gr.Chatbot(value=[[None, initial_message_sinhala], [None, list(questions_sinhala.keys())[0]]], height=600)


def read_openapi_key():
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    # Read the properties file
    config.read('config.properties')
    # Get encryption key from properties file
    encryption_key = config.get('encryption', 'key')
    # Get encrypted value from properties file
    encrypted_value = config.get('encrypted', 'value')
    return decrypt_value(encryption_key.encode(), encrypted_value)


def filter(choice):
    global questions
    global language_input_var
    if choice == "English":
        questions = questions_english
        language_input_var = "English"
        return [gr.update(visible=True), gr.update(visible=False)]
    elif choice == "සිංහල":
        questions = questions_sinhala
        language_input_var = "සිංහල"
        return [gr.update(visible=False), gr.update(visible=True)]


def form_question():
    formed_question = ""
    begin_message_english = "Generate a financial advice report in the context of Sri Lankan investment and wealth " \
                              "generation options, for given information as question and answer pairs. Report should " \
                              "consists of minimum of 1000 words and maximum 2000 words.\n"

    begin_message_sinhala = "ප්‍රශ්න සහ පිළිතුරු යුගල වශයෙන් ලබා දී ඇති තොරතුරු සඳහා ශ්‍රී ලංකාවේ ආයෝජන සහ ධන " \
                              "උත්පාදන විකල්පයන් සම්බන්ධයෙන් මුල්‍ය උපදේශන වාර්තාවක් සකස් කරන්න. වාර්තාව අවම වශයෙන් " \
                              "වචන 1000කින් සහ උපරිම වචන 2000කින් සමන්විත විය යුතුය. \n"

    if language_input_var == 'English':
        formed_question = begin_message_english
    elif language_input_var == 'සිංහල':
        formed_question = begin_message_sinhala

    for key, value in questions.items():
        if value and value.strip():
            formed_question = formed_question + "\n" + key + ": " + value

    print(formed_question)
    return formed_question


def initialize_questions():
    global questions
    questions = {}


def chatbot_response(input):
    if input:
        try:
            messages[1] = {"role": "user", "content": input}
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            reply = chat.choices[0].message.content

            initialize_questions()

            if language_input_var == 'English':
                reply = report_heading_english + reply
            elif language_input_var == 'සිංහල':
                reply = report_heading_sinhala + reply

            return reply
        except Exception as e:
            print(e)
            return "Something went wrong!"


def respond(message, chat_history):
    initial_message = ""
    if language_input_var == 'English':
        initial_message = initial_message_english
    elif language_input_var == 'සිංහල':
        initial_message = initial_message_sinhala

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
    initial_message = ""
    if language_input_var == 'English':
        initial_message = initial_message_english
    elif language_input_var == 'සිංහල':
        initial_message = initial_message_sinhala
    chat_history.clear()
    chat_history.append((None, initial_message))
    chat_history.append((None, list(questions.keys())[0]))
    return "", chat_history


with gr.Blocks() as demo:
    gr.Markdown("""# Financial ChatBot""")

    language_options = ["English", "සිංහල"]
    language_input = gr.Radio(choices=language_options, label="Please select the language you wish to continue")
    # language_input.change(disable_language_selection, inputs=[language_input], outputs=[language_input])

    with gr.Column(visible=True) as colA:
        questionnaire_english.render()
        msg = gr.Textbox()
        btn = gr.Button(value="Clear")
        btn.click(clear_chatbot, inputs=[msg, questionnaire_english],
                  outputs=[msg, questionnaire_english])
        msg.submit(respond, [msg, questionnaire_english],
                   [msg, questionnaire_english], scroll_to_output=True)
    with gr.Column(visible=False) as colB:
        questionnaire_sinhala.render()
        msg = gr.Textbox()
        btn = gr.Button(value="Clear")
        btn.click(clear_chatbot, inputs=[msg, questionnaire_sinhala],
                  outputs=[msg, questionnaire_sinhala])
        msg.submit(respond, [msg, questionnaire_sinhala],
                   [msg, questionnaire_sinhala], scroll_to_output=True)

    language_input.change(filter, language_input, [colA, colB])
    # list(questions.keys())[0]]

    # chatbot = gr.Chatbot(value=[[None, initial_message], [None, list(questions.keys())[0]]], height=600)

if __name__ == "__main__":
    openai.api_key = read_openapi_key()
    demo.launch()
