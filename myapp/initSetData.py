from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import OuterRef, Subquery
from .models import Attendance, Parent, Child
import json
from .initChildren import initChildren
from .setDummyData import setDummyData

initChildren()

setDummyData()