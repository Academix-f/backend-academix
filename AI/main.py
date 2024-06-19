import os
from dotenv import load_dotenv
import google.generativeai as gemini_embedder
from PIL import Image
import io

load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMNI_API_KEY') 


#this is a method that makes embeddings/the vectors 
def embed(object):
    result = (gemini_embedder.embed_content(
        model="models/embedding-001",
        content= object,
        task_type="retrieval_document",))
    
    return result['embedding']

# def in_memory_file_to_bytes(in_memory_file):
#     try:
#         image = Image.open(in_memory_file)
#         image_bytes = image.tobytes()
#         return image_bytes
#     except OSError:
#         return None

def is_image(object):
    try:
        img = Image.open(object)
        return True
    except OSError:
        return False
    