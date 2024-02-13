# Import forms module from django to create form classes.
from django import forms
# Import the models from the current package to use them in form definitions.
from . import models        

# Define TicketForm, a ModelForm for creating or editing Ticket instances.
class TicketForm(forms.ModelForm):
    class Meta:
        # Specify the model to which this form is linked.
        model = models.Ticket
        # Define the fields from the Ticket model that should be included in this form.
        fields = ['title', 'description', 'image']

# Define ReviewForm, a ModelForm for creating or editing Review instances.
class ReviewForm(forms.ModelForm):
    # Define a BooleanField to track if the review is being edited, hidden by default.
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    # Define a ChoiceField for rating with predefined choices and a custom widget.
    rating = forms.ChoiceField(
        label='Rating',
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect(attrs={'class': 'rating-buttons'}),
    )

    class Meta:
        # Specify the model to which this form is linked.
        model = models.Review
        # Define the fields from the Review model that should be included in this form.
        fields = ['headline', 'rating', 'body']

# Define DeleteReviewForm, a simple form for confirming review deletion.
class DeleteReviewForm(forms.Form):
    # Define a BooleanField to confirm deletion, hidden by default.
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

# Define SearchUsersForm, a Form for user search functionality.
class SearchUsersForm(forms.Form):
    # Define a CharField for inputting a username to search, with a label and maximum length.
    search_user = forms.CharField(label='Search for username', max_length=100,
                                  widget=forms.TextInput(attrs={'id': 'search-user'}))
