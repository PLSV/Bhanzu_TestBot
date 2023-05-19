import openai
import os
import json


def setup():
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    # openai_organisation_id = os.environ.get('OPENAI_ORGANISATION_ID')
    openai.api_key = openai_api_key
    # openai.organization = openai_organisation_id


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


def get_completion_without_context(prompt, model="gpt-3.5-turbo", temperature=1):
    setup()
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.get("content")


if __name__ == "__main__":
    prompt = f"""
    
    your task is to create json of list of questions with following parameters:
        1. there will be total of 10 questions
        2. There will be a total of 4 options, out of which only one is the right answer.
        3. each option will be a json object with key as A B C D and value as the answer.
        3. Please ensure that the wrong answers will be as close to the right answer as possible.
        4. the mathematics concepts will be based on the 4th grade students.
        5. provide one correct option for each question 
        """
    model_rep = get_completion_without_context(prompt)
    question_json = None
    try:
        question_json = json.loads(model_rep)
    except TypeError:
        print("not json")
    print(question_json)