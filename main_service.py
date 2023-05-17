import utilities as util
import database_utilities as dbutil
import openai_service as aiservice
import prompt_completions as prompts


def main_function():
    try:
        starting_prompt = dbutil.get_from_db("test_chat")
        if not starting_prompt:
            starting_prompt = [{
                                "role": "system",
                                "content": prompts.set_role_prompt({
                                    "no_of_questions": 5
                                })
                            }]
            dbutil.add_to_db("test_chat", starting_prompt)
        response = aiservice.get_completion_from_messages(messages=starting_prompt)
        starting_prompt.append(response)
        dbutil.add_to_db("test_chat", starting_prompt)
        print(response)
        return response
    except Exception as e:
        print("Encountered an exception", e)