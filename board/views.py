import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from streamlit import status

from .forms import *
from .models import *
from .serializers import *


# Create your views here.
def board_list(request):
    board=Board.objects.all()
    # serializer=BoardSerializer(board,many=True)
    board=Board.objects.all().values('id', 'title', 'content','user','date', 'generation').order_by('-pk')
    # return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({'board_list':list(board)})

@csrf_exempt
def board_upload(request):
    if request.method=="POST":
        data=json.loads(request.body)
        board_upload=Board.objects.create(title=data['title'],content=data['content'],user=request.user.id,generation=data['generation'],date=timezone.now())
        return JsonResponse({
            "id":board_upload.id,
            "title":board_upload.title,
            "content":board_upload.content,
            "user":board_upload.user.id,
            "date":board_upload.date,
            "generation":board_upload.generation
        })
    return JsonResponse({"error":"Post 요청만 가능"},status=405)

def board_detail(request,pk):
    try:
        board=Board.objects.get(id=pk)
        return JsonResponse({
            "id":board.id,
            "title":board.title,
            "content":board.content,
            "user":board.user.id,
            "date":board.date,
            "generation":board.generation
        })
    except Board.DoesNotExist:
        return JsonResponse({"error":"게시글 없음"},status=404)

@csrf_exempt
def board_edit(request,pk):
    if request.method=='PUT':
        try:
            board=get_object_or_404(Board, id=pk)
            data=json.loads(request.body)
            board.title=data['title']
            board.content=data['content']
            board.user=request.user.id
            board.date=timezone.now()
            board.save()
            return JsonResponse({
                "id":board.id,
                "content":board.content,
                "user":board.user,
                "date":board.date,
                "generation":board.generation
            })
        except Board.DoesNotExist:
            return JsonResponse({"error":"게시글을 찾을 수 없음"},status=404)
    return JsonResponse({"error":"PUT 요청만 가능"})


@csrf_exempt
def board_delete(request, pk):
    if request.method=='DELETE':
        try:
            board = get_object_or_404(Board, id=pk)
            board.delete()
            return JsonResponse({
            "id":board.id,
            "title":board.title,
            "content":board.content,
            "user":board.user.id,
            "date":board.date,
            "generation":board.generation
            })
        except Board.DoesNotExist:
            return JsonResponse({"error":"게시글을 찾을 수 없음"},status=404)
    return JsonResponse({"error":"DELETE 요청만 가능"},status=405)


def page_view(request):
    paginator = Paginator(board, 10)  # (데이터, 페이지당 보여줄 데이터 개수) #p
    page_number = request.GET.get('page') #now page
    page_obj = paginator.get_page(page_number)
    info=paginator.get_page(page_number)#둘이같은건가

    start_page=(int(page_number)-1)//10*10+1
    end_page=start_page+9
    if end_page>paginator.num_pages:
        end_page=paginator.num_pages
    page_range=range(start_page,end_page+1)

    return JsonResponse({"info":info,"page_range":page_range})


def like(request, pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소 (remove)
            article.like_users.remove(request.user)
            status='unlike'
        else:
            # 좋아요 추가 (add)
            article.like_users.add(request.user)
            status='like'
        return JsonResponse({
            "status":status,
            "like_count": like_count,
        })
    return JsonResponse({"error": "login required"}, status=401)
