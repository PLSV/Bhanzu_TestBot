import boto3
from reportlab.pdfgen import canvas

def string_to_pdf(input_string, filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, input_string)
    c.save()

def upload_to_s3(filename, bucket_name, object_name):
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(filename, bucket_name, object_name)
    return response