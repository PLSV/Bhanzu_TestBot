import utils.utility as util
import utils.database_utility as dbutil
import services.openai_service as aiservice
import prompt_completions as prompts
from exceptions.application_exception import ApplicationException

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

def get_questions():
    quiz_chat = dbutil.get_from_db("quiz_chat")
    quiz_chat.extend([
        {
            "role": "user",
            "content": prompts.get_question_prompt()
        }
    ])
    response = aiservice.get_completion_from_messages(messages=quiz_chat)
    quiz_chat.append(response)
    dbutil.add_to_db("quiz_chat", quiz_chat)
    questions = util.extract_json_from_string(response.get("content"))
    print(questions)
    dbutil.add_to_db("questions", questions)
    return questions

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

def capture_answer(question_index, choice, explanation):
    try:
        questions = dbutil.get_from_db("questions")
        if not questions:
            raise ApplicationException("You have not fetched the questions yet. Please do so by entering the command get questions", 400)
        question = questions[question_index-1].get("Question")
        answer = questions[question_index-1].get("Options")[choice-1]
        response = {
            "question_no": question_index,
            "question": question,
            "chosen_answer": answer,
            "explanation": explanation
        }
        answers_data = dbutil.get_from_db("answers")
        if not answers_data:
            dbutil.add_to_db("answers", [response])
        else:
            answers_data.append(response)
            dbutil.add_to_db("answers", answers_data)
        return response
    except IndexError as e:
        raise ApplicationException(f"Invalid question number or choice. Please enter a valid question number or the correct choice", 400)
    except Exception as e:
        raise ApplicationException(f"Encountered an exception of type {e}")


def submit_answers(only_evaluate=False):
    answers = dbutil.get_from_db("answers")
    quiz_chat = dbutil.get_from_db("quiz_chat")
    quiz_chat.extend([
        {
            "role": "user",
            "content": prompts.submit_answers_prompt(answers)
        }
    ])
    response = aiservice.get_completion_from_messages(messages=quiz_chat)
    if not only_evaluate:
        quiz_chat.append(response)
        dbutil.add_to_db("quiz_chat", quiz_chat)
        dbutil.add_to_db("test_report", response)
    return response


def get_next_question(question_number):
    questions = dbutil.get_from_db("questions")
    if not questions:
        raise ApplicationException("You have not fetched the questions yet. Please do so by entering the command get questions", 400)
    if question_number < len(questions):
        return questions[question_number], True
    return None, False


def generate_scope_of_improvement():
    scope_of_improvement = dbutil.get_from_db("scope_of_improvement")
    if scope_of_improvement:
        return scope_of_improvement
    improvement_prompt = prompts.generate_improvement_prompt()
    quiz_chat = dbutil.get_from_db("quiz_chat")
    quiz_chat.extend([
        {
            "role": "user",
            "content": improvement_prompt
        }
    ])
    response = aiservice.get_completion_from_messages(messages=quiz_chat)
    quiz_chat.append(response)
    dbutil.add_to_db("quiz_chat", quiz_chat)
    dbutil.add_to_db("scope_of_improvement", response)
    return response


def generate_study_plan():
    study_plan = dbutil.get_from_db("study_plan")
    if study_plan:
        return study_plan
    study_prompt = prompts.generate_study_plan_prompt()
    quiz_chat = dbutil.get_from_db("quiz_chat")
    quiz_chat.extend([
        {
            "role": "user",
            "content": study_prompt
        }
    ])
    response = aiservice.get_completion_from_messages(messages=quiz_chat)
    quiz_chat.append(response)
    dbutil.add_to_db("quiz_chat", quiz_chat)
    dbutil.add_to_db("study_plan", response)
    return response