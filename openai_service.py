import openai
import os

def setup():
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    openai_organisation_id = os.environ.get('OPENAI_ORGANISATION_ID')
    openai.api_key = openai_api_key
    openai.organization = openai_organisation_id

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=1):
    setup()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    to_return = response.choices[0].message
    return {
        "content": to_return.get("content"),
        "role": to_return.get("role")
    }