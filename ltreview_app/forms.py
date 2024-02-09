from django import forms
from . import models        


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    rating = forms.ChoiceField(
        label='Rating',
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect(attrs={'class': 'rating-buttons'}),)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class SearchUsersForm(forms.Form):
    search_user = forms.CharField(label='Search for username', max_length=100,
                                  widget=forms.TextInput(attrs={'id': 'search-user'}))
