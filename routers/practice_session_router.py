from fastapi import Request, APIRouter
from services.test_service import TestService
from utils.models import UserData
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/practice")

templates = Jinja2Templates(directory="templates")


def prepare_question_page_html(question_json, question_number, request):
    question_text = question_json["Question"]
    options = question_json["Options"]
    template_dict = {"question_number": question_number, "request": request}
    template_dict.update({"question_text": question_text})
    options_vars = dict([(f"option_{option_index+1}",
                          options[option_index]) for option_index, option in enumerate(options)])
    template_dict.update(options_vars)
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
    print("fddc")
    forma_dara = await request.form()
    print(forma_dara)

    # todo: capture the user response and generate the next question if not all questions are answered
    #  other wise call the evaluation method and return the final result with feedback

    pass
