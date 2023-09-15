from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import OuterRef, Subquery
from .models import Attendance, Parent, Child
import json
import math
import random

class setDummyData:
    reasons = [
        "体調不良", "子供の意志", "保護者の体調不良", "法事", "お出かけ"
    ]
    def __init__(self):
        Attendance.objects.all().delete()
        children = Child.objects.all()
        attendance = Attendance(
            child=children[0], 
            attendance=2, 
            datetime = timezone.now()
        )
        try:
            # データベースに登録
            attendance.save()
        except Exception as e:
            print(f"########## エラー内容 ############\n{e}\n##########################")
        for child in children[1:len(children)]:
            rnd_attendance  = math.floor(random.random() * 3)
            if rnd_attendance == 0:
                rnd_reason = math.floor(random.random() * len(self.reasons))
                rnd_reply = math.floor(random.random() * 2)
                if rnd_reply == 0:
                    attendance = Attendance(
                        child=child, 
                        attendance=0, 
                        reason=self.reasons[rnd_reason],
                        reply="確認済み",
                        datetime = timezone.now()
                    )
                else:
                    attendance = Attendance(
                        child=child, 
                        attendance=0, 
                        reason=self.reasons[rnd_reason],
                        datetime = timezone.now()
                    )
            else:
                attendance = Attendance(
                    child=child, 
                    attendance=rnd_attendance, 
                    reason="",
                    datetime = timezone.now()
                )
            try:
                # データベースに登録
                attendance.save()
            except Exception as e:
                print(f"########## エラー内容 ############\n{e}\n##########################")
            

        