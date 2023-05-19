from services import prompt_service


class TestService:

    @staticmethod
    def generate_test(user_data):
        prompt_service.introfunction(user_data)
        prompt_service.quizmaster_setup()
        questions_list = prompt_service.get_questions()
        return questions_list

    @staticmethod
    def capture_answer(option_chosen, question_number, reason):
        option_index_map = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
        option_index = option_index_map.get(option_chosen, None)
        prompt_service.capture_answer(question_number, option_index, reason)
        next_question, question_found = prompt_service.get_next_question(question_number)
        return next_question

    @staticmethod
    def get_result(only_evaluate=False):
        test_result = prompt_service.submit_answers(only_evaluate)
        return test_result
