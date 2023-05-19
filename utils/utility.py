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