from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import *
from django.shortcuts import get_object_or_404
from pgvector.django import L2Distance
from AI.main import embed
from RequestApp.models import Notification
from UserApp.models import MyUser

#++++++++++++++++++++ POST METHODS +++++++++++++++++++++++++++

#----------------- create club -------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated , IsAdminUser])
def create_club(request):
    serializer = ClubSerializer(data= request.data)

    if serializer.is_valid():
        serializer.save(founder = request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def create_club_from_request(req):
    club = req.club #club jason
    club['founder'] = req.student
    is_funder = Club.objects.filter(founder = club['founder']).first()

    if not is_funder:
        club_obj = Club(name = club['name'] , founder = club['founder'] , overview = club['overview'])
        notify = Notification(to_user=req.student, status=2, content="Request Aproved")
        notify.save()
        club_obj.save()
   
#=============================================================================

#------------------------- create section -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_section(request):
    request_data = request.data
    serializer = SectionSerializer(data= request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#=============================================================================

#----------------------- create event ------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    request_data = request.data
    serializer = EventSerializer(data= request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_event_from_request(req):
    event =req.event

    event_obj = Event(club_id = event['club'] , building = event['building'],start_time = event['start_time'] , end_time = event['end_time'] , description = event['description'])
    print(event_obj.__dict__)
    notify = Notification(to_user = req.student , status = 2 , content = "Request Aproved")
    notify.save()
    event_obj.save()
   

#=============================================================================


#+++++++++++++++++++++++ GET METHODS ++++++++++++++++++++++++++++

#---------------- get club -------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_club(request , pk):
    club = get_object_or_404(Club , id = pk)
    serializer = ClubSerializer(instance=club)

    return Response(serializer.data , status=status.HTTP_200_OK)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_clubs(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(instance= clubs , many = True)

    return Response({'clubs': serializer.data} , status=status.HTTP_200_OK)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_club(request , pk):
    club = get_object_or_404(Club , id = pk)
    text = f"Club named: {club.name}, overview: {club.overview}"

    search_embedding = embed(text)
    clubs = Club.objects.order_by(L2Distance('embedding' , search_embedding))[:10]

    serializer = ClubSerializer(instance=clubs , many = True)

    return Response(serializer.data , status= status.HTTP_200_OK)
  

#===================================================================


#----------------------- get section -----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated , IsAdminUser])
def get_section(request , pk):
    section = get_object_or_404(Section , id = pk)
    serializer = ClubSerializer(instance=section)

    return Response(serializer.data , status=status.HTTP_200_OK)

def get_all_section(request , pk):
    sections = Section.objects.all()
    serializer = SectionSerializer(instance=sections , many = True)

    return Response({'sections':serializer.data} , status=status.HTTP_200_OK)

#=========================================================


#-----------------------get event------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event(request , pk):
    event = get_object_or_404(Event , id = pk)
    serializer = ClubSerializer(instance=event)

    if serializer.is_valid():
        return Response(serializer.data , status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(instance=events , many = True)

    return Response({'events':serializer.data} , status=status.HTTP_200_OK)
 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_events(request , pk):
    event = get_object_or_404(Event , id = pk)

    text = f"Event starting at: {event.start_time}, description: {event.description}"
    request_embedding = embed(text)

    events = Event.objects.order_by(L2Distance('embedding' , request_embedding))[:10]
    serializer = EventSerializer(instance=events , many = True)

    return Response({'events': serializer.data} , status=status.HTTP_200_OK)

#=========================================================================


#+++++++++++++++++++++++++ UPDATE METHODES ++++++++++++++++++++++++++++++


#------------------- update club ----------------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_club(request, pk):
    club = get_object_or_404(Club , id = pk)
    serializer = ClubSerializer(instance=club , data= request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
#=========================================================================

#------------------------- update section ---------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_section(request, pk):
    section = get_object_or_404(Section , id = pk)
    serializer = SectionSerializer(instance=section , data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

#=========================================================================

#----------------------------- update event ------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    event = get_object_or_404(Event , id = pk)
    serializer = EventSerializer(instance=event , data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

#=========================================================================

#++++++++++++++++++++++++ DELETE METHODES +++++++++++++++++++++++++++++++

#------------------------- delete club -----------------------------------

@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_club(request , pk):
    club = get_object_or_404(Club , id = pk)
    serializer = ClubSerializer(instance=club)
    serialized_data = serializer.data 
    club.delete()
    return Response({'deleted_club': serialized_data} , status=status.HTTP_202_ACCEPTED)

#===========================================================================

#------------------------- delete section ----------------------------------

@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_section(request , pk):
    section = get_object_or_404(Section, id = pk)
    serializer = SectionSerializer(instance=section)
    serialized_data = serializer.data 
    section.delete()
    return Response({'deleted_section': serialized_data} , status=status.HTTP_202_ACCEPTED)

#============================================================================

#-------------------------- delete event ------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_event(request , pk):
    event = get_object_or_404(Event, id = pk)
    serializer = EventSerializer(instance=event)
    serialized_data = serializer.data 
    event.delete()
    return Response({'deleted_event': serialized_data} , status=status.HTTP_202_ACCEPTED)

#============================================================================