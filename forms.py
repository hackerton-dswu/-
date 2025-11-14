from django.forms import ModelForm
from board.models import *
# from fileupload.models import FileUpload
from django import forms

class BoardForm(ModelForm): # BoardForm 클래스는 ModelForm 클래스를 상속받음. 이 클래스를 사용하면 Board 모델의 필드와 동일한 이름을 가진 HTML form 요소를 쉽게 생성할 수 있음. 이 폼으로부터 제출된 데이터는 Board 모델 객체로 변환하여 데이터베이스에 저장할 수 있음.
    class Meta: # Meta: 클래스 변수, 폼에 대한 설정을 담고 있음(모델 폼의 메타데이터를 담고 있는 클래스).
        model = Board   # 이 폼이 사용할 모델을 Board 모델로 지정함
        fields=['title','content'] # 이 폼에서 사용할 필드=사용자가 입력할 수 있는 필드. user는 뷰에서 처리함

# class FileUploadForm(ModelForm):
#     class Meta:
#         model = FileUpload
#         fields=['title','imgfile','content']

class CommentForm(forms.ModelForm):
    content_comment=forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':3,
            'placeholder':'comment',
        })
        # lable은 없고 placeholder는 comment인 textarea를 렌더링
    )
    class Meta:
        model=Comments
        fields=['content_comment']