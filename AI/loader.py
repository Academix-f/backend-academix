#methods from this module will be used to load contexts and generaet text from other file types mainly image
from BasicApp.models import *
from CommunityApp.models import *
from PostApp.models import *
from pgvector.django import L2Distance

def load_all(question):
    #gets the top 10 simmilar objects with the prompt_embedding and merges thier description and content
    prompt_embedding = main.embed(question)
    courses = Course.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    departments = Department.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    buildings = Building.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    clubs = Club.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    events = Event.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    posts = Post.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    comments = Comment.objects.order_by(L2Distance('embedding' , prompt_embedding))[:10]
    res = []

    for course in courses:
        res.append(course.overview )

    for department in departments:
        res.append(department.overview )

    for club in clubs:
        res.append(club.overview)

    for building in buildings:
        res.append(building.description)
    
    for event in events:
        res.append(event.description)
    
    for post in posts:
        res.append(post.content)
    
    for comment in comments:
        res.append(comment.content)
    
    
    return res





    