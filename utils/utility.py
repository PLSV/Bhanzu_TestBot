import boto3
from reportlab.pdfgen import canvas
import re
import json
from exceptions.application_exception import ApplicationException


def string_to_pdf(input_string, filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, input_string)
    c.save()


def upload_to_s3(filename, bucket_name, object_name):
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket_name, object_name)
    return response

def extract_json_from_string(string_with_json):
    json_pattern = r"<JSON>(.*?)<\/JSON>"
    json_match = re.search(json_pattern, string_with_json, re.DOTALL)

    if json_match:
        extracted_text = json_match.group(1)
        cleaned_json = re.sub(r"\s+", " ", extracted_text)
        json_data = json.loads(cleaned_json)
        return json_data
    else:
        raise ApplicationException("No JSON found in the string", 400)