from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import OuterRef, Subquery
from .models import Attendance, Parent, Child
import json


##########################
# 出欠情報を登録するAPI
##########################
@csrf_exempt  # これでCSRFのセキュリティロックを無効化する
def regist_attendance(request):
    if request.method == "POST":
        # json.loadsでrequestのbodyを取得しないと、キーをもとに値を取り出せない
        request_body = json.loads(request.body)

        # キーをもとにrequestのbodyからほしい値を取得
        child_id = request_body.get("child_id")
        attendance_value = request_body.get("attendance")
        reason_value = request_body.get("reason")

        # 該当のchild_idをもつAttendanceレコードの中で最新のものを取得
        attendance = Attendance.objects.filter(child=child_id).latest('datetime')
        attendance.attendance = attendance_value
        attendance.reason = reason_value
        attendance.datetime = timezone.now()
        attendance.reply = ""

        try:
            # データベースに登録
            attendance.save()
            return HttpResponse(True)
        except Exception as e:
            print(f"########## エラー内容 ############\n{e}\n##########################")
            return HttpResponse(False)


##########################
# 出欠情報を取得するAPI
##########################
@csrf_exempt
def return_status(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        child_id = request_body.get("child_id")
        try:
            # child_id
            status = Attendance.objects.filter(child=child_id).latest('datetime')
        except Attendance.DoesNotExist:
            return JsonResponse(
                data={},
                status=404
            )
        data = {
            "child_name" : status.child.name,
            "attendance" : status.attendance,
            "datetime" : status.datetime.strftime('%Y年%m月%d日　%H : %M'),
            "reason" : status.reason,
            "reply" : status.reply,
        }
        return JsonResponse(data=data)


##########################
# 児童一覧を返すAPI
##########################
@csrf_exempt
def return_children(request):
    if request.method == "GET":
        try:
            children = Attendance.objects.all()
            child_ids = []
            for obj in children:
                if not (obj.child in child_ids):
                    child_ids.append(obj.child)

            data = {"attending_children": [], "absent_children": [], "empty_children": []}
            for child_id in child_ids:
                obj = Attendance.objects.filter(child=child_id).latest('datetime')
                if f'{obj.datetime}'[0:10] == f'{timezone.now()}'[0:10] and obj.attendance == "1":
                    data["attending_children"].append({
                        "child_id": obj.child.id, 
                        "child_name": obj.child.name, 
                        "attendance": obj.attendance, 
                        "reason": obj.reason, 
                        "datetime": obj.datetime.strftime('%Y年%m月%d日　%H : %M'),
                        "reply": obj.reply,
                    })
                elif f'{obj.datetime}'[0:10] == f'{timezone.now()}'[0:10] and obj.attendance == "0":
                    data["absent_children"].append({
                        "child_id": obj.child.id, 
                        "child_name": obj.child.name, 
                        "attendance": obj.attendance, 
                        "reason": obj.reason, 
                        "datetime": obj.datetime.strftime('%Y年%m月%d日　%H : %M'),
                        "reply": obj.reply,
                    })
                elif f'{obj.datetime}'[0:10] == f'{timezone.now()}'[0:10] and obj.attendance == "2":
                    data["empty_children"].append({
                        "child_id": obj.child.id, 
                        "child_name": obj.child.name, 
                        "attendance": obj.attendance, 
                        "reason": obj.reason, 
                        "datetime": obj.datetime.strftime('%Y年%m月%d日　%H : %M'),
                        "reply": obj.reply,
                    })
        except Attendance.DoesNotExist:
            return JsonResponse(
                data={},
                status=404
            )

        return JsonResponse(data=data, safe=False)


##########################
# 更新するAPI
##########################
@csrf_exempt  # これでCSRFのセキュリティロックを無効化する
def update_reply(request):
    if request.method == "POST":
        # json.loadsでrequestのbodyを取得しないと、キーをもとに値を取り出せない
        request_body = json.loads(request.body)

        reply_value = ""

        # キーをもとにrequestのbodyからほしい値を取得
        try:
            child_id = request_body.get("child_id")
        except Exception as e:
            print(f"########## エラー内容 ############\n{e}\n##########################")
        try:
            reply_value = request_body.get("reply")
        except Exception as e:
            print(f"########## エラー内容 ############\n{e}\n##########################")
        
        parent = Parent(id=1, name="parent1")
        child = Child(id=child_id, parent=parent, name=f"child{child_id}")
        
        attendance = Attendance.objects.filter(child=child_id).latest('datetime')
        attendance.reply = reply_value

        try:
            # データベースに登録
            attendance.save()
            return HttpResponse(True)
        except Exception as e:
            print(f"########## エラー内容 ############\n{e}\n##########################")
            return HttpResponse(False)