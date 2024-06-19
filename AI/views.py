import AI
import AI.general
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view

gemini = AI.general.LLM()

@api_view(['POST'])
def chat_api(request):
    print(request)
    question = request.data['question']
    response = gemini.chat(question)

    return Response({'answer' : response} , status= status.HTTP_200_OK)
