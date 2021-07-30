from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from random import choice
import markdown2
import os

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label='content', widget=forms.Textarea())

class SearchWiki(forms.Form):
    query = forms.CharField(label='query', max_length=100, help_text="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            'title': title,
            'data': markdown2.markdown(util.get_entry(title))
        })
    else:
        # Create HTML page for nothing found, with option to submit
        return render(request, "encyclopedia/entry.html", {
            'tab_title' : "Entry not found.",
            'title': 'Looks like this page does not exist or it\'s empty!',
            'data': 'Nothing to see here.'
        })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

            return render(request, 'encyclopedia/new.html', {
                "new_entry" : NewEntryForm()
            })
    return render(request, 'encyclopedia/new.html', {
        "new_entry" : NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

    if request.method == 'GET':
        entry = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            "entry" : NewEntryForm(initial={
                'title':title.capitalize(),
                'content': entry
            })
        })
    return render(request, 'encyclopedia/new.html', {
        "new_entry" : NewEntryForm()
    })

    return HttpResponse("Hello")

def random_page(request):
    title = choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        'title' : title.lower(),
        'data' : markdown2.markdown(util.get_entry(title))
    })

def search(request):
    if request.method == 'POST':
        form = SearchWiki(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query in util.list_entries():
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[query]))

            else:
                return render(request, 'encyclopedia/search.html', {
                    "entries": util.search_entries(query),
                    "query": query
                })
        else:
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))