from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import io
import base64
import requests

API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
HEADERS = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    return response.content

def home(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        resolution = data.get('image-aspect-ratio', '1080x1080')
        if prompt:
            image_bytes = query({"inputs": prompt})

            image = Image.open(io.BytesIO(image_bytes))
            img_io = io.BytesIO()
            image.save(img_io, format='PNG')
            img_io.seek(0)
            image_data = base64.b64encode(img_io.read()).decode('utf-8')

            return JsonResponse({
                'prompt': prompt,
                'image_data': image_data,
            })
    return render(request, 'index.html')
