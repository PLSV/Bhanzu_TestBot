import boto3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
import re
import json
from exceptions.application_exception import ApplicationException


def string_to_pdf(input_string, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 10)
    x = 10
    y = 750
    max_width = 550
    lines = simpleSplit(input_string, 'Helvetica', 10, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= 12
    c.save()
    return filename


def upload_to_s3(filename):
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(filename, "hackathon-worksheet", filename)
        return f"https://hackathon-worksheet.s3.us-east-2.amazonaws.com/{filename}"
    except Exception as e:
        raise ApplicationException("Error uploading file to S3", 400)


def extract_json_from_string(string_with_json):
    try:
        json_pattern = r"<JSON>(.*?)<\/JSON>"
        json_match = re.search(json_pattern, string_with_json, re.DOTALL)
        print("json_match: ", json_match)
        if json_match:
            extracted_text = json_match.group(1)
            cleaned_json = re.sub(r"\s+", " ", extracted_text)
            print("cleaned_json: ", cleaned_json)
            json_data = json.loads(cleaned_json)
            print("formatted_json: ", json_data)
            return json_data
        else:
            raise ApplicationException("No JSON found in the string", 400)
    except Exception as e:
        return extract_json_from_json_regexp(string_with_json)


def extract_json_from_json_regexp(string_with_json):
    start_index = string_with_json.find("[")
    end_index = string_with_json.rfind("]") + 1

    json_string = string_with_json[start_index:end_index]
    data = json.loads(json_string)
    print(data)
    return data