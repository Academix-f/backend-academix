from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializer import StudentSerializer, AdminSerializer, MyUserSerializer
from .models import Student, Admin, MyUser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from CommunityApp.models import Section


@api_view(['POST'])
def signUp(request):
    '''student signup route'''

    fields = set(['student_id', 'academic_year', 'semester', 'department', 'section'])

    hashmap = {key: value for key, value in request.data.items() if key not in fields}
    newMap = {key: value for key, value in request.data.items() if key in fields}

    serializer = MyUserSerializer(data=hashmap)
    student = StudentSerializer(data=newMap)

    newMap.pop('section')

    if serializer.is_valid() and student.is_valid():
        user = serializer.save()
        student1 = student.save()
        user.set_password(request.data['password'])
        user.student = student1
        section = Section.objects.filter(name=request.data['section'], year=user.student.academic_year, department=user.student.department).first()
        if not section:
            section = Section(year=user.student.academic_year, department=user.student.department, name=request.data['section'])
            section.rep = user
            section.save()
            user.student.is_rep = True
        user.student.section = section
        user.student.save()
        user.save()
        serializer = MyUserSerializer(instance=user)
        serializer_copy = serializer.data.copy()
        serializer_copy['student'] = StudentSerializer(instance=student1).data
        token = Token.objects.create(user=user)

        return Response({"Token": token.key, "user": serializer_copy}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    '''student and admin login route'''

    username = request.data['username']
    password = request.data['password']

    user = MyUser.objects.filter(username=username).first()
    if user and user.check_password(password):
        serializer = MyUserSerializer(instance=user)
        token, create = Token.objects.get_or_create(user=user)
        serializer_copy = serializer.data

        if user.is_staff:
            serializer_copy['admin'] = AdminSerializer(instance=user.admin).data
        else:
            serializer_copy['student'] = StudentSerializer(instance=user.student).data
        
        return Response({"Token": token.key, "user": serializer_copy}, status=status.HTTP_201_CREATED)
    return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    '''token tester'''
    return Response(f"pass {request.user.student.student_id}", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    '''logout route'''

    Token.objects.filter(user=request.user).delete()
    return Response("successfully logged out", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = MyUser.objects.filter(is_staff=False)
    all_users = []
    for user in users:
        UserSerializer = MyUserSerializer(instance=user)
        dic = UserSerializer.data
        # print(user, user.student)
        dic['student'] = StudentSerializer(instance=user.student).data
        all_users.append(dic)
    
    return Response({"students": all_users}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_staff_users(request):
    users = MyUser.objects.filter(is_staff=True)
    all_users = []
    for user in users:
        UserSerializer = MyUserSerializer(instance=user)
        dic = UserSerializer.data
        # print(user, user.student)
        dic['admin'] = AdminSerializer(instance=user.admin).data
        all_users.append(dic)
    
    return Response({"admin": all_users}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_some_users(request):
    username = request.data.get('username')
    department = request.data.get('department')
    academic_year = request.data.get('academic_year')

    query = Q(department=department) | Q(username=username) | Q(academic_year=academic_year)

    users = MyUser.objects.filter(query)
    all_users = []
    for user in users:
        UserSerializer = MyUserSerializer(instance=user)
        dic = UserSerializer.data
        dic['student'] = StudentSerializer(instance=user.student).data
        all_users.append(dic)
    
    return Response({"students": all_users}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_counts(request):
    print('hello')
    new_dict = {
        "first_year": MyUser.objects.filter(is_staff=False, student__academic_year=1).count(),
        "second_year": MyUser.objects.filter(is_staff=False, student__academic_year=2).count(),
        "third_year": MyUser.objects.filter(is_staff=False, student__academic_year=3).count(),
        "forth_year": MyUser.objects.filter(is_staff=False, student__academic_year=4).count(),
        "fifth_year": MyUser.objects.filter(is_staff=False, student__academic_year=5).count(),
        "female": MyUser.objects.filter(is_staff=False, gender='f').count(),
        "male": MyUser.objects.filter(is_staff=False, gender='m').count(),
        "total": MyUser.objects.filter(is_staff=False).count(),
    }

    return Response({"data": new_dict}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    user = get_object_or_404(MyUser, id=id)

    if request.method == 'DELETE' and request.user.is_staff:
        user.student.delete()
        user.delete()
        return Response("deleted successfully", status=status.HTTP_200_OK)
    elif request.method == 'POST':
        fields = set(['student_id', 'academic_year', 'semester', 'department', 'section'])

        hashmap = {key: value for key, value in request.data.items() if key not in fields}
        newMap = {key: value for key, value in request.data.items() if key in fields}

        serilizer = MyUserSerializer(user, data=hashmap)
        serilizer2 = StudentSerializer(user.student, data=newMap)

        if serilizer.is_valid() and serilizer2.is_valid():
            updated_user = serilizer.save()
            updated_student = serilizer2.save()

            serializer = MyUserSerializer(instance=updated_user)
            serializer_copy = serializer.data.copy()
            serializer_copy['student'] = StudentSerializer(instance=updated_student).data
        
            return Response({"user": serializer_copy}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        user1 = MyUserSerializer(instance=user).data
        return Response({'user': user1}, status=status.HTTP_200_OK)
    return Response({"error": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


    



        
