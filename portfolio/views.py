import requests
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PortfolioCategory, PortfolioImage, PortfolioSliderImage, AboutMe
from .forms import PortfolioImageAddForm, PortfolioCategoryAddForm, PortfolioSliderImageAddForm, FeedbackForm, AboutMeForm
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.core.exceptions import ObjectDoesNotExist


def portfolio_greeting_page(request):
    slider_images = PortfolioSliderImage.objects.all()
    context = {'slider_images': slider_images,
               }
    return render(request, 'portfolio/portfolio_greeting_page.html', context)


def portfolio_image_list(request, category_slug=None):
    category = None
    categories = PortfolioCategory.objects.all()
    images = PortfolioImage.objects.all()
    quantity = len(images)

    query = request.GET.get('q')
    if query:
        images = images.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    if category_slug:
        category = get_object_or_404(PortfolioCategory, slug=category_slug)
        images = PortfolioImage.objects.filter(category=category)
        quantity = len(images)
    context = {'category': category,
               'categories': categories,
               'images': images,
               'quantity': quantity,
               }
    return render(request, 'portfolio/portfolio_home.html', context)


def portfolio_image_create(request):
    if not request.user.is_superuser:
        raise Http404
    form = PortfolioImageAddForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Success!')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request, 'Something Went Wrong!')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_image_create_form.html', context)


def portfolio_image_update(request, image_id, image_slug):
    instance = get_object_or_404(PortfolioImage, id=image_id, slug=image_slug)
    if not request.user.is_superuser:
        raise Http404
    form = PortfolioImageAddForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Updated!')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'portfolio/portfolio_image_create_form.html', context)


def portfolio_image_detail(request, image_id, image_slug):
    instance = get_object_or_404(PortfolioImage, id=image_id, slug=image_slug)
    if not request.user.is_staff or not request.user.is_superuser:
        instance.views += 1
        instance.save()
    context = {
        'instance': instance,
    }
    return render(request, 'portfolio/portfolio_image_detail.html', context)


def portfolio_image_clear_views(request, image_id, image_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortfolioImage, id=image_id, slug=image_slug)
    instance.views = 0
    instance.save()
    return HttpResponseRedirect(instance.get_absolute_url())


def portfolio_image_delete(request, image_id, image_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortfolioImage, id=image_id, slug=image_slug)
    instance.delete()
    messages.success(request, 'Successfully Deleted!')
    return redirect('portfolio:portfolio_image_list')


def portfolio_category_list(request):
    categories = PortfolioCategory.objects.all()
    images = PortfolioImage.objects.all()
    context = {
        'categories': categories,
        'images': images,
    }
    return render(request, 'portfolio/portfolio_category_list.html', context)


def portfolio_category_create(request):
    if not request.user.is_superuser:
        return render(request, 'portfolio/staff_only.html')
    form = PortfolioCategoryAddForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created!')
        return redirect('portfolio:portfolio_category_list')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_category_create_form.html', context)


def portfolio_category_update(request, category_conf_slug):
    if not request.user.is_superuser:
        return render(request, 'portfolio/staff_only.html')
    instance = get_object_or_404(PortfolioCategory, slug=category_conf_slug)
    form = PortfolioCategoryAddForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('portfolio:portfolio_category_list')
    context = {
        'instance': instance,
        'form': form,
    }
    return render(request, 'portfolio/portfolio_category_create_form.html', context)


def portfolio_category_detail(request, category_conf_slug):
    instance = get_object_or_404(PortfolioCategory, slug=category_conf_slug)
    context = {
        'instance': instance
    }
    return render(request, 'portfolio/portfolio_category_detail.html', context)


def portfolio_category_delete(request, category_conf_slug):
    if not request.user.is_staff or not request.user.is_superuser:
        return render(request, 'portfolio/staff_only.html')
    instance = get_object_or_404(PortfolioCategory, slug=category_conf_slug)
    instance.delete()
    messages.success(request, 'Successfully Deleted!')
    return redirect('portfolio:portfolio_category_list')


def portfolio_slider_images_list(request):
    slider_images = PortfolioSliderImage.objects.all()
    context = {
        'slider_images': slider_images,
    }
    return render(request, 'portfolio/portfolio_slider_images_list.html', context)


def portfolio_slider_images_create(request):
    if not request.user.is_superuser:
        raise Http404
    form = PortfolioSliderImageAddForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Success!')
        return redirect('portfolio:portfolio_slider_images_list')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_slider_image_create_form.html', context)


def portfolio_slider_images_update(request, slider_id):
    instance = get_object_or_404(PortfolioSliderImage, id=slider_id)
    if not request.user.is_superuser:
        raise Http404
    form = PortfolioSliderImageAddForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Success!')
        return redirect('portfolio:portfolio_slider_images_list')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_slider_image_create_form.html', context)


def portfolio_slider_images_delete(request, slider_id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortfolioSliderImage, id=slider_id)
    instance.delete()
    messages.success(request, 'Successfully Deleted!')
    return redirect('portfolio:portfolio_slider_images_list')


def contact(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        sender = form.cleaned_data['sender']
        message = form.cleaned_data['message']
        copy = form.cleaned_data['copy']
        recipients = ['tony1986@yandex.ru', 'olga.podustova@gmail.com']
        if copy:
            recipients.append(sender)
        context = {
            'message': 'Successfully sent! Thank you!',
            'sender': sender,
        }
        requests.post(
            "https://api.mailgun.net/v3/olgapodustova.herokuapp.com/messages",
            auth=("api", "key-*********************************"),
            data={"from": "Olga Podustova <postmaster@olgapodustova.herokuapp.com>",
                  "to": recipients,
                  "subject": subject,
                  "text": message + '\n______________' + '\nSent from: ' + sender}
        )
        return render(request, 'portfolio/contact_form_send_success.html', context)
    context = {
        'form': form,
    }
    return render(request, 'portfolio/contact_form.html', context)


def about_me(request):
    about_me = AboutMe.objects.all()
    trigger = len(about_me)
    context = {
        'about_me': about_me,
        'trigger': trigger,
    }
    return render(request, 'portfolio/portfolio_about_me.html', context)


def about_me_create(request):
    if not request.user.is_superuser:
        raise Http404
    form = AboutMeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Success!')
        return redirect('portfolio:about_me')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_about_me_form.html', context)


def about_me_update(request, about_me_id):
    instance = get_object_or_404(AboutMe, id=about_me_id)
    if not request.user.is_superuser:
        raise Http404
    form = AboutMeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Success!')
        return redirect('portfolio:about_me_update')
    context = {
        'form': form,
    }
    return render(request, 'portfolio/portfolio_about_me_form.html', context)
