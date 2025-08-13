from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['body'].widget.attrs.update({
            'placeholder': 'Share your thoughts on this horror film...',
            'class': 'comment-textarea'
        })
