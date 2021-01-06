import markdown2
from django.shortcuts import render
from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import random

class newForm(forms.Form):
    title=forms.CharField(label="Title")
    content=forms.CharField(widget=forms.Textarea(attrs={"style":"height:500px"}))

class newEditForm(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={"style":"height:500px"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def newpage(request):
    if request.method == "POST":
        form = newForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            if util.get_entry(title) == None :
                util.save_entry(title,content)

            else:

                return render(request,"encyclopedia/duplicateerror.html", {
                    "entryname" : title
                })
                

            # If valid, redirect to the entry page
            return entry(request,title)

        else:

            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": newForm()
    })

def entry(request, entrytitle):
    if util.get_entry(entrytitle)==None:
        return render(request,"encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", {
        "entrycontent" : markdown2.markdown(util.get_entry(entrytitle)),
        "entrytitle" : entrytitle.capitalize()
    })

def search(request):
    query = request.GET.get('q')
    if util.get_entry(query) == None:

        #Here, there is no exact result.
        entriesList = util.list_entries()
        possibleEntriesList = [] #This will be a list with all the possible entries
        for entries in entriesList:
            is_similar=True
            for letterIndex in range(0,len(query)):
                try:
                    if query[letterIndex].lower() != entries[letterIndex].lower():
                        is_similar = False
                except IndexError:
                    is_similar=False 
            if is_similar:
                possibleEntriesList.append(entries)
        return render(request,"encyclopedia/search.html", {
            "entriesList":possibleEntriesList
        })




    return render(request, "encyclopedia/entry.html", {
        "entrycontent" : markdown2.markdown(util.get_entry(query)),
        "entrytitle" : query.capitalize()
    })

def randomPage(request):
    pageList=util.list_entries()
    randomPageIndex=random.randint(0,len(pageList)-1)
    randomPage = pageList[randomPageIndex]
    return render(request, "encyclopedia/entry.html", {
        "entrycontent" : markdown2.markdown(util.get_entry(randomPage)),
        "entrytitle" : randomPage.capitalize()
    })

def editEntry(request,entrytitle):
    if request.method == "POST":

        form = newEditForm(request.POST)

        if form.is_valid():

            content=form.cleaned_data["content"]

            util.save_entry(entrytitle,content)
            return entry(request,entrytitle)

        else:

            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

    return render(request, "encyclopedia/edit.html", {
        "form" : newEditForm({'content':util.get_entry(entrytitle)}),
        "entrytitle" : entrytitle
    })