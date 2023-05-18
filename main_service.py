import utilities as util
import database_utilities as dbutil
import openai_service as aiservice
import prompt_completions as prompts
from application_exception import ApplicationException

def quizmaster_setup():
    try:
        intro_prompt = dbutil.get_from_db("intro_message")
        if not intro_prompt:
            raise ApplicationException("You have not introduced yourself yet. Please do so by entering your name, grade and teacher", 400)
        starting_prompt = dbutil.get_from_db("quiz_chat")
        starting_prompt.extend([
            {
                "role": "system",
                "content": prompts.setup_roleplay_prompt()
            },
            {
                "role": "user",
                "content": prompts.set_role_prompt({
                    "no_of_questions": 5
                })
            },
            {
                "role": "assistant",
                "content": "Understood. I shall wait for your instructions."
            },
            {
                "role": "user",
                "content": prompts.get_options_for_student()
            }
        ])
        dbutil.add_to_db("quiz_chat", starting_prompt)
        response = aiservice.get_completion_from_messages(messages=starting_prompt)
        starting_prompt.append(response)
        dbutil.add_to_db("quiz_chat", starting_prompt)
        return response
    except Exception as e:
        return {"Error": f"Encountered an exception of type {e}"}

quizmaster_setup()

def introfunction(intro_payload):
    try:
        intro = dbutil.get_from_db("intro_message")
        if intro:
            return {"response": f"You have already introduced yourself. your name is {intro['name']} and you belong to the grade {intro['grade']}. You are taught by {intro['teacher']}."}
        dbutil.add_to_db("intro_message", intro_payload)
        intro_prompt = prompts.get_intro_prompt(intro_payload)
        quiz_prompt = dbutil.get_from_db("quiz_chat")
        if not quiz_prompt:
            quiz_prompt = [{
                "role": "user",
                "content": intro_prompt
            }]
            dbutil.add_to_db("quiz_chat", quiz_prompt)
        response = aiservice.get_completion_from_messages(messages=quiz_prompt, temperature=0)
        quiz_prompt.append(response)
        dbutil.add_to_db("quiz_chat", quiz_prompt)
        return {"response": response["content"]}
    except Exception as e:
        raise ApplicationException(f"Encountered an exception of type {e}")