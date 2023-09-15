from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import OuterRef, Subquery
from .models import Attendance, Parent, Child
import json

class initChildren:
    child_names = [
        "田中太郎",
        "佐藤太郎",
        "高橋花子",
        "伊藤太郎",
        "渡辺太郎",
        "山本太郎",
        "中村太郎",
        "小林太郎",
        "加藤太郎",
        "吉田花子",
        "山田花子",
        "佐々木花子",
        "山口花子",
        "松本花子",
        "井上花子",
        "木村花子",
        "林花子",
        "斎藤花子",
        "清水花子",
        "山崎太郎",
        "森花子",
        "池田太郎",
        "橋本花子",
        "阿部太郎",
        "山下花子",
        "中島太郎",
        "石井花子",
        "小川太郎"
    ]

    def __init__(self):
        Child.objects.all().delete()
        i = 0
        for child_name in self.child_names:
            i += 1
            parent = Parent(id=1, name="parent1")
            child = Child(id=f'{i}', parent=parent, name=child_name)
            try:
                # データベースに登録
                child.save()
            except Exception as e:
                print(f"########## エラー内容 ############\n{e}\n##########################")