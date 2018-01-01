import os
import random
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from xmas_happiness_engine.static.static_dirs.pics.outloc import PICLOC
from xmas_happiness_engine.matching import tought_to_memory
from xmas_happiness_engine.models import Note, Memory
from xmas_happiness_engine.serializers import NoteSerializer

def index(request):
    return render(request, 'index.html', {})

@login_required()
def thought_to_memory(request, thought):

    thought = thought.replace("-"," ")
    memory = {}
    memory_df = tought_to_memory(thought)
    memory['date'] = list(memory_df.loc[:,'date'])[0].strftime('%d/%m/%Y')
    memory['messages'] = {}

    for index, row in memory_df.iterrows():
        message = {}
        message['author'] = row['author']
        message['message'] = row['message']
        memory['messages'][str(index)] = message

    r, c = shuffle_pics(request)

    pics = {}
    pics['chen'] = str(c) + '.jpg'
    pics['ric'] = str(r) + '.jpg'
    memory['pics'] = pics
    memory['thought'] = thought
    mem_to_data = json.dumps(memory)
    data_mem = Memory.objects.create(
        memory=mem_to_data
    )
    memory['id'] = data_mem.id

    return JsonResponse(memory)

@login_required()
def datab_to_memory(request, mem_id):

    data_mem = get_object_or_404(Memory, id=mem_id)

    memory = json.loads(data_mem.memory)

    return JsonResponse(memory)

@login_required()
def shuffle_pics(request):

    RIC = PICLOC+'/ric'
    CHEN = PICLOC+'/chen'
    RICpics = [file for file in os.listdir(RIC) if file.endswith('jpg')]
    CHENpics = [file for file in os.listdir(CHEN) if file.endswith('jpg')]

    r = random.choice(range(1,len(RICpics)+1))
    c = random.choice(range(1,len(CHENpics)+1))

    return r,c

@login_required
@api_view(['POST'])
def post_note(request):

    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        serializer.initial_data['user'] = str(request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET'])
def get_all_notes(request):

    notes = Note.objects.all().order_by('created').reverse()
    serializer = NoteSerializer(notes, many=True)

    return JsonResponse(serializer.data, safe=False)

