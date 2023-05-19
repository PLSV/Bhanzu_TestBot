from fastapi import Request, APIRouter
from services.test_service import TestService
from utils.models import UserData
from fastapi.templating import Jinja2Templates
from utils import utility
from fastapi.responses import JSONResponse

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
        "result_page.html", template_dict)


@router.post("/receive/user")
async def get_question(request: Request):
    # todo: read user details from form, prepare set of questions and send the first question
    forma_dara = await request.form()
    name = forma_dara.getlist('fname')[0]
    grade = forma_dara.getlist('fgrade')[0]
    teacher = forma_dara.getlist('fteacher')[0]
    user_data = UserData(grade=grade, name=name, teacher=teacher)
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


@router.get("/evaluate_response")
async def evaluate_response(request: Request):
    result = TestService.get_result(only_evaluate=True)
    # result = prepare_result_page(request)
    return result


@router.post("/improvement_plan")
async def get_improvement_plan():
    result = TestService.get_improvement_plan()
    file_name = utility.string_to_pdf(result, "improvement_plan.pdf")
    file_url = utility.upload_to_s3(file_name)
    return JSONResponse({"file_url": file_url})


@router.post("/improvement_scope")
async def get_improvement_scope():
    result = TestService.get_improvement_scope()
    file_name = utility.string_to_pdf(result, "improvement_plan.pdf")
    file_url = utility.upload_to_s3(file_name)
    return JSONResponse({"file_url": file_url})