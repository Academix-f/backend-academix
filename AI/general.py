import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from . import loader
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from PIL import Image
import google.generativeai as vision
import io
from . import main

load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMNI_API_KEY')
VISION_API_KEY = os.getenv('GEMNI_VISION_API_KEY')

#this whole class is intended to contain the ai functionalities we want chat and content verification 
class LLM:
    def __init__(self):
        self._systemMessage = SystemMessage(content = """You serve as an assistant chatbot on a web-based social media platform,
                                            specifically tailored for Ethiopian university students.""" )
        
        self._template = """ The student has asked you this question : {question},
                            If the question you are asked falls with in this context : {context}, 
                            Your answer should be based on that and kindly provide more information about the topic from your training data.
                            If the question is not related to the provided context ,simply reply just 'No' """
    
        self._output = StrOutputParser()
        self._llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
        self.prompt = PromptTemplate.from_template(system_message = self._systemMessage, template = self._template)
    

    def get_context(self , question):
        context_list = loader.load_all(question)
        return context_list
   
    def chat(self , question):
        chain = self.prompt | self._llm | self._output
        answer = chain.invoke({
            "question": question,
            "context": self.get_context(question)
        })


        # model = vision.GenerativeModel('gemini-pro')

        if answer.strip().lower() == "no":
            template = """ Answer this question , question : {question}, """
            prompt = PromptTemplate.from_template(system_message = self._systemMessage, template = template)
            chain = prompt | self._llm | self._output

            answer = chain.invoke({
                "question": question,
            })

            answer = f""" This inquiry can not be found in the Academix data base but, based on my understanding, {answer} """
 
            
        return answer

    

    def verify_test_content(self, content):
        
        systemMessage = SystemMessage( content="""You are now configured to operate as a strict content classifier.
                                            Your responses must be limited to a single word that best classifies the content presented to you.""")
        

        template = """Classify this content : {content} as, 'Educational' or 'Non-Educational'"""
        prompt = PromptTemplate.from_template(systemmessage = systemMessage , template=template)

        chain = prompt | self._llm | self._output

        if chain.invoke(content) == "Educational":
            return True
        else:
            return False


    def verify_image_content(self, path):
        model = vision.GenerativeModel('gemini-pro-vision')
        prompt = "Classify this image as 'Educational' or 'Non educational' "

        img = Image.open(path)
        res = model.generate_content([prompt , img])

        print(res.text)
        if res.text.strip() == "Educational":
            return True
        else:
            return False
        
    def image_report(self , path):
        model = vision.GenerativeModel('gemini-pro-vision')
        
        img = Image.open(path)
        prompt = "Explain the contents of this image"
        res = model.generate_content([prompt , img])

        return res.text

     

    
