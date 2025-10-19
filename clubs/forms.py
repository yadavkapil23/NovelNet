from django import forms
from .models import BookClub, ClubDiscussion


class BookClubForm(forms.ModelForm):
    """Form for creating/editing book clubs."""
    class Meta:
        model = BookClub
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter club name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your book club...'
            })
        }


class ClubDiscussionForm(forms.ModelForm):
    """Form for creating club discussions."""
    class Meta:
        model = ClubDiscussion
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Discussion title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Share your thoughts...'
            })
        }
