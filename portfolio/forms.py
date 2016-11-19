from django import forms
from .models import PortfolioImage, PortfolioCategory, PortfolioSliderImage, Feedback, AboutMe


class PortfolioImageAddForm(forms.ModelForm):
    class Meta:
        model = PortfolioImage
        fields = [
            'category',
            'name',
            'image',
            'description',
        ]


class PortfolioCategoryAddForm(forms.ModelForm):
    class Meta:
        model = PortfolioCategory
        fields = [
            'name',
            'description',
        ]


class PortfolioSliderImageAddForm(forms.ModelForm):
    class Meta:
        model = PortfolioSliderImage
        fields = [
            'name',
            'image',
            'image_text',
        ]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'subject',
            'sender',
            'message',
            'copy',
        ]


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = [
            'title',
            'image',
            'about_me'
        ]
