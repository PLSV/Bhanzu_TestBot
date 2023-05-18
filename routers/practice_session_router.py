from fastapi import Request, APIRouter
from services.test_service import TestService
from utils.models import UserData
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/practice")

templates = Jinja2Templates(directory="templates")


def prepare_question_page_html(question_json, question_number, request, test_id="dummy_test_id"):
    question_text = question_json["Question"]
    options = question_json["Options"]
    template_dict = {"question_number": question_number, "request": request, "test_id": test_id}
    template_dict.update({"question_text": question_text})
    options_vars = dict([(f"option_{option_index+1}",
                          options[option_index]) for option_index, option in enumerate(options)])
    template_dict.update(options_vars)
    return templates.TemplateResponse(
        "question_page.html", template_dict)


def prepare_result_page(request):
    template_dict = {"request": request}
    return templates.TemplateResponse(
        "question_page.html", template_dict)


@router.get("/receive/user")
async def get_question(request: Request):
    # todo: read user details from form, prepare set of questions and send the first question
    user_data = UserData(grade=6, name="amit", teacher="amitt")
    questions_list = TestService.generate_test(user_data.dict())
    question_page = prepare_question_page_html(questions_list[0], 1, request)
    return question_page


@router.post("/capture/response")
async def capture_response(request: Request):
    forma_dara = await request.form()
    print(forma_dara)
    option_chosen = forma_dara.getlist('option_chosen')[0]
    question_number = int(forma_dara.getlist('question_number')[0])
    reason = forma_dara.getlist('reason')[0]
    next_question = TestService.capture_answer(option_chosen, question_number, reason)
    if next_question:
        question_page = prepare_question_page_html(next_question, question_number+1, request)
        return question_page
    else:
        result = TestService.get_result()
        return result
        # result_page = prepare_result_page(request)
        # return result_page
