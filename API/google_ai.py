import json

import google.generativeai as genai

genai.configure(api_key="AIzaSyCeN2-R6tDr3_2GxLOPHIrG593e0k11t-Q")  # This key might be in .env file

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
    ]
)


def send_prompt(text):
    response = chat_session.send_message(text)
    formatted_response = response.to_dict()
    return formatted_response['candidates'][0]['content']['parts'][0]['text']
