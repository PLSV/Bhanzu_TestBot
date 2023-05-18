from services import prompt_service


class TestService:

    @staticmethod
    def generate_test(user_data):
        prompt_service.introfunction(user_data)
        prompt_service.quizmaster_setup()
        questions_list = prompt_service.get_questions()
        return questions_list

