def set_role_prompt(prompt_parameters):
    question_prompt = \
        f"""
        I am going to give you a set of instructions that you will abide by as a quizmaster_setup as shown below:
        
        1. You are going to generate a total of {prompt_parameters.get("no_of_questions", 5)} Multiple Choice Questions.
        2. There will be a total of 5 options, out of which only one is the right answer.
        3. Please ensure that the wrong answers will be as close to the right answer as possible.
        4. The mathematics concepts will be based on the grade that was mentioned earlier.
        5. You will be expecting an answer, that is, one of the 5 options and an explanation for the chosen option.
        6. You will be evaluating not only the option chosen, you will also evaluate the explanation for the answer given and give a rating from 0 to 10.
        7. If there is no explanation provided, irrespective of the choice made, you will award 0 points for explanation and 0 for the question irrespective of whether the choice made was correct or not.
        8. Once an answer is given for a particular question, you will keep a record of it and not tell what the correct answer is. Only after all the answers are given will you be revealing the correct answers and the score that you have given for the explanation given.
        9. However, you can reveal the scores if you receive the response 'End Test'. This response can be case insensitive.
        10. You will be giving a score for the explanation given for the answer. This score will be from 0 to 10.
        11. Please generate the questions only when you hear the response 'Generate Questions'. This response can be case insensitive.
        12. Please send the generated questions to me in the JSON format as shown below: 
            {get_generated_questions_json()}
        Please confirm if you have understood the instructions and await further instructions.
        """

    return question_prompt


def retrieve_topics_prompt(topics):
    topics_prompt = f"""
        Topics to choose from are:
        """

    for each in topics:
        topics_prompt += f"\n- {each}"

    return topics_prompt


def generate_study_plan_prompt():
    return """
    Can you give me a study plan for improvement based on the said topics? Given that I am free for these hours for each day of the week as shown below:
    
    Monday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM.
    Tuesday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM.
    Wednesday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM.
    Thursday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM.
    Friday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM.
    Saturday: 1:00 PM - 5:00 PM, 7:30 PM - 9:00 PM.
    Sunday: 10:00 AM - 2:00 PM, 3:00 PM - 6:00 PM, 7:30 PM - 9:00 PM.
    """


def generate_improvement_prompt():
    return """
    Please give me a detailed report on what I need to improve upon. Please give it to me in the following format. 
    
    ```Topic: Scope for improvement```
    
    The topic is the one based on which the questions were asked. Please do not include any websites for reference. Just add in books to read.
    
    The scope for improvement will be based on the explanation I had given for my choice for all the questions.
    """


def get_intro_prompt(intro_parameters):
    return f"""Hello, my name is {intro_parameters["name"]} and I belong to the grade {intro_parameters["grade"]}. I am being taught by {intro_parameters["teacher"]}. Nice to meet you!!"""


def setup_roleplay_prompt():
    return "Let's do some role-play. I want you to take on the role of a quizmaster_overseeing a quiz on mathematics."


def get_generated_questions_json():
    return """
        [
            {
                "Question": "Question text",
                "Options": [Option 1, Option 2, Option 3 ...]
            },
            {
                "Question": "Question text",
                "Options": [Option 1, Option 2, Option 3 ...]
            },
            ...
            {
                "Question": "Question text",
                "Options": [Option 1, Option 2, Option 3 ...]
            }
        ]
    """


def get_options_for_student():
    return """
    Please give the following options to the participant:
    1. Revaluate Results: On choosing this option, you will check if the results are correct once again by going through the answers given.
    2. End Test: On choosing this option, you will end the test and reveal the results to the participant.
    """

def get_question_prompt():
    return f"""
    Based on the instructions given earlier, your task is to create json of list of questions based on the format below:
    
    {get_generated_questions_json()}

    Ensure that the json object is enclosed in between '<JSON>' and '</JSON>'.
    """


def submit_answers_prompt(answers):
    return f"""
    These are the answers in the JSON format:
    
    {answers}
    
    Please evaluate the answers and give a score for the explanation given for the answer. This score will be from 0 to 10.
    """