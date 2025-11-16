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
    board = Board.objects.all()
    # serializer=BoardSerializer(board,many=True)
    board = Board.objects.all().values('id', 'title', 'content', 'user', 'date', 'generation').order_by('-pk')
    # return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    return JsonResponse({'board_list': list(board)})


@csrf_exempt
def board_upload(request):
    if request.method == "POST":
        data = json.loads(request.body)
        board_upload = Board.objects.create(
            title=data['title'],
            content=data['content'],
            user=request.user,
            generation=data['generation'],
            date=timezone.now()
        )
        return JsonResponse({
            "id": board_upload.id,
            "title": board_upload.title,
            "content": board_upload.content,
            "user": board_upload.user_id,
            "date": board_upload.date,
            "generation": board_upload.generation
        })
    return JsonResponse({"error": "Post 요청만 가능"}, status=405)


def board_detail(request, pk):
    try:
        board = Board.objects.get(id=pk)
        return JsonResponse({
            "id": board.id,
            "title": board.title,
            "content": board.content,
            "user": board.user_id,
            "date": board.date,
            "generation": board.generation
        })
    except Board.DoesNotExist:
        return JsonResponse({"error": "게시글 없음"}, status=404)


@csrf_exempt
def board_edit(request, pk):
    if request.method == 'PUT':
        try:
            board = get_object_or_404(Board, id=pk)
            data = json.loads(request.body)
            board.title = data['title']
            board.content = data['content']
            board.user = request.user
            board.date = timezone.now()
            board.save()
            return JsonResponse({
                "id": board.id,
                "title": board.title,
                "content": board.content,
                "user": board.user_id,
                "date": board.date.isoformat(),
                "generation": board.generation
            })
        except Board.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "PUT 요청만 가능"})


@csrf_exempt
def board_delete(request, pk):
    if request.method == 'DELETE':
        try:
            board = get_object_or_404(Board, id=pk)
            board.delete()
            return JsonResponse({
                "id": board.id,
                "title": board.title,
                "content": board.content,
                "user": board.user_id,
                "date": board.date,
                "generation": board.generation
            })
        except Board.DoesNotExist:
            return JsonResponse({"error": "게시글을 찾을 수 없음"}, status=404)
    return JsonResponse({"error": "DELETE 요청만 가능"}, status=405)


def page_view(request):
    qs = Board.objects.all()
    paginator = Paginator(qs, 10)  # (데이터, 페이지당 보여줄 데이터 개수) #p
    page_number = int(request.GET.get('page', 1))  # now page
    page_obj = paginator.page(page_number)

    start_page = int(((page_number) - 1) // 10 * 10 + 1)
    end_page = start_page + 9
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages
    page_range = list(range(start_page, end_page + 1))

    boards = []
    for board in page_obj:
        boards.append({
            'id': board.id,
            'title': board.title,
            "content": board.content,
            "user": board.user_id,
            "date": board.date.isoformat(),
            "generation": board.generation
        })

    return JsonResponse({
        # "page": paginator,
        'boards':boards,
        "page_number": page_number,
        "total_page":paginator.num_pages,
        "has_previous":page_obj.has_previous(),
        "has_next":page_obj.has_next(),
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range
    })


def like(request, pk):
    if request.user.is_authenticated:
        board = get_object_or_404(Board, pk=pk)
        # board = Board.objects.get(pk=pk)
        if board.like.filter(pk=request.user.id).exists():
            # 좋아요 취소 (remove)
            board.like.remove(request.user)
            status = 'unlike'
        else:
            # 좋아요 추가 (add)
            board.like.add(request.user)
            status = 'like'
        return JsonResponse({
            "id": board.id,
            "status": status,
            "like_count": board.like_count,
        })
    return JsonResponse({"error": "login required"}, status=401)
