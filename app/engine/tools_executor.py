import os
import csv, json, pypdf
from docx import Document
import openai
from anthropic import Anthropic
from mistralai import Mistral

# def execute_file_input(path_to_file):
#     if not os.path.isfile(path_to_file):
#         raise FileNotFoundError(path_to_file)
#     file_extension = os.path.splitext(path_to_file)[-1].lower()
#     # print(file_extension)
#
#     if file_extension in ['.txt', '.log']:
#         with open(path_to_file, mode='r', encoding='utf-8') as f:
#             return f.read()
#     elif file_extension in ['.json']:
#         with open(path_to_file, mode='r', encoding='utf-8') as f:
#             data = json.loads(f.read())
#             return json.dumps(data, indent=4)
#     elif file_extension in ['.csv']:
#         text_output = []
#         with open(path_to_file, mode='r', encoding='utf-8') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 text_output.append(', '.join(row))
#         return '\n'.join(text_output)
#     elif file_extension in ['.pdf']:
#         text_output = []
#         with open(path_to_file, mode='rb') as f:
#             reader = pypdf.PdfReader(f)
#             for page in reader.pages:
#                 text_output.append(page.extract_text() or "")
#         return '\n'.join(text_output)
#     elif file_extension in [".docx"]:
#         doc = Document(path_to_file)
#         # doc = docx.getdocumenttext(path_to_file)
#         return "\n".join([para.text for para in doc.paragraphs])

def execute_file_input(file_text):
    return file_text

def execute_chat_input(text):
    # if not text:
    #     raise FileNotFoundError(text)
    return text

def execute_llm(model_name, file_input=None, chat_input=None, api_key=None, system_prompt=None):
    if not api_key:
        raise ValueError("API key is required")
    if not (file_input or chat_input):
            raise ValueError("Either chat input or file input is required")
    messages = []
    if file_input:
        _text = execute_file_input(file_input)
        messages.append({"role": 'user', "content":_text})
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": chat_input})
    # # open a gemini client and run the query
    # if model_name.lower()=="gemini":
    #     client = GeminiClient(api_key=api_key)
    #     response = client.chat.create(
    #         model="gemini",  # Replace with appropriate Gemini model name
    #         messages=messages
    #     )
    #     return response["choices"][0]["content"]  # Adjust based on actual response format
    #
    #
    if model_name.lower()=="gpt-3.5-turbo":
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
            # prompt=chat_input
        )
        return response["choices"][0]["content"]
    if model_name.lower()=="mistral":
        client = Mistral(api_key=api_key)
        messages.append({"role": "system", "content": chat_input})
        response = client.chat.complete(
            model = "mistral-small",
            messages = messages
        )
        return response.choices[0].message.content
    if model_name.lower() in ["claude-2", "claude-3"]:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model = model_name,
            messages = [{"role": "system", "content": chat_input},{"role": "user", "content": file_input}],
            max_tokens=4096
        )
        return response.content[0].text
    else:
        raise ValueError("Model not supported")

# def chat_response_generator(chat_id, user_chat_message):
#
#
#

# if __name__ == "__main__":
#     text = execute_file_input(r'/test.docx')
#     # print(text)
#     t = execute_llm("mistral-7b", r'/test.docx', "hi, please analyze this and give me a one line answer on what this is.", "LqlGQaD5YIcu0RtSVejsrZbWJcH83m0a")
#     # print(type(t))
#     print(t)