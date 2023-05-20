from fastapi import Request, APIRouter
from services.test_service import TestService
from utils.models import UserData
from fastapi.templating import Jinja2Templates
from utils import utility
from fastapi.responses import JSONResponse
from services import voice_service
import threading


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


def prepare_result_page(request, result):
    template_dict = {"request": request, "result": result}
    thread = threading.Thread(target=voice_service.read_report, args=(result,))
    thread.start()
    return templates.TemplateResponse(
        "result_page.html", template_dict)


@router.post("/receive/user")
async def get_question(request: Request):
    # todo: read user details from form, prepare set of questions and send the first question
    forma_dara = await request.form()
    voice_service.request_user_to_wait()
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
        voice_service.ask_user_to_wait_for_results()
        result = TestService.get_result()
        result_page = prepare_result_page(request, result)
        return result_page


@router.post("/report")
async def evaluate_response(request: Request):
    result = TestService.get_result(only_evaluate=True)
    file_name = utility.string_to_pdf(result, "worksheet_report.pdf")
    file_url = utility.upload_to_s3(file_name)
    return JSONResponse({"response": result, "file_url": file_url})


@router.post("/plan")
async def get_improvement_plan():
    result = TestService.get_improvement_plan()
    file_name = utility.string_to_pdf(result, "improvement_plan.pdf")
    file_url = utility.upload_to_s3(file_name)
    return JSONResponse({"file_url": file_url})


@router.post("/scope")
async def get_improvement_scope():
    result = TestService.get_improvement_scope()
    file_name = utility.string_to_pdf(result, "improvement_scope.pdf")
    file_url = utility.upload_to_s3(file_name)
    return JSONResponse({"file_url": file_url})