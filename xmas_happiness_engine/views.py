import os
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from xmas_happiness_engine.static.static_dirs.pics.outloc import PICLOC
from .matching import tought_to_memory

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
