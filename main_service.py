import utilities as util
import database_utilities as dbutil
import openai_service as aiservice
import prompt_completions as prompts


def quizmaster():
    try:
        starting_prompt = dbutil.get_from_db("quiz_chat")
        if not starting_prompt:
            starting_prompt = [{
                                "role": "system",
                                "content": prompts.set_role_prompt({
                                    "no_of_questions": 5
                                })
                            }]
            dbutil.add_to_db("quiz_chat", starting_prompt)
        response = aiservice.get_completion_from_messages(messages=starting_prompt)
        starting_prompt.append(response)
        dbutil.add_to_db("quiz_chat", starting_prompt)
        return response.dict()
    except Exception as e:
        return {"Error": f"Encountered an exception of type {e}"}
        
def introfunction(intro_payload):
    try:
        intro = dbutil.get_from_db("intro_message")
        if intro:
            return {"prompt_response": f"You have already introduced yourself. your name is {intro['name']} and you are {intro['age']} years old"}
        dbutil.add_to_db("intro_message", intro_payload)
        intro_prompt = prompts.get_intro_prompt(intro_payload)
        quiz_prompt = dbutil.get_from_db("quiz_chat")
        if not quiz_prompt:
            quiz_prompt = [{
                "role": "user",
                "content": intro_prompt
            }]
            dbutil.add_to_db("quiz_chat", quiz_prompt)
        response = aiservice.get_completion_from_messages(messages=quiz_prompt)
        quiz_prompt.append(response)
        dbutil.add_to_db("quiz_chat", quiz_prompt)
        return {"response": response["content"]}
    except Exception as e:
        return {"Error": f"Encountered an exception of type {e}"}

        