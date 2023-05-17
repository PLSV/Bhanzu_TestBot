def set_role_prompt(prompt_parameters):
    question_prompt = \
        f"""
        I am going to give you a set of instructions that you will abide by as a quizmaster as shown below:
        
        1. You are going to generate a total of {prompt_parameters.get("no_of_questions", 5)} Multiple Choice Questions.
        2. There will be a total of 5 options, out of which only one is the right answer
        3. The mathematics concepts will be based on the grade that was mentioned earlier.
        4. You will be expecting an answer, that is, one of the 5 options and an explanation for the chosen option.
        5. You will be evaluating not only the option chosen, you will also evaluate the explanation for the answer given and give a rating from 0 to 10.
        6. If there is no explanation provided, irrespective of the choice made, you will award 0 points for explanation and 0 for the question irrespective of whether the choice made was correct or not.
        7. Once an answer is given for a particular question, you will keep a record of it and not tell what the correct answer is. Only after all the answers are given will you be revealing the correct answers and the score that you have given for the explanation given. 
        8. You will reveal the questions that are unanswered if you receive the response, 'Unanswered Questions'. This response can be case insensitive.
        9. However, you can reveal the scores if you receive the response 'End Test'. This response can be case insensitive.
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
    
    Monday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM
    Tuesday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM
    Wednesday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM
    Thursday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM
    Friday: 5:30 PM - 8:00 PM, 10:00 PM - 11:00 PM
    Saturday: 1:00 PM - 5:00 PM, 7:30 PM - 9:00 PM
    Sunday: 10:00 AM - 2:00 PM, 3:00 PM - 6:00 PM, 7:30 PM - 9:00 PM
    """


def generate_improvement_prompt():
    return """
    Please give me a detailed report on what I need to improve upon. Please give it to me in the following format. 
    
    ```Topic: Scope for improvement```
    
    The topic is the one based on which the questions were asked. Please do not include any websites for reference. Just add in books to read
    
    The scope for improvement will be based on the explanation I had given for my choice for all the questions
    """


def get_intro_prompt(intro_parameters):
    return f"""Hello, my name is {intro_parameters["name"]} and I belong to the grade {intro_parameters["grade"]}. I am being taught by {intro_parameters["teacher"]}. Nice to meet you!!"""


def setup_roleplay_prompt():
    return "Let's do some role-play. I want you to take on the role of a quizmaster overseeing a quiz on mathematics."