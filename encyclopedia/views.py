import random

from django.shortcuts import render, redirect

from . import util
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        content = util.get_entry(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": util.convert_md_to_html(content)
        })
    else:
        return render(request, "encyclopedia/not-found.html")
    
def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, "encyclopedia/search.html", {
            "query": "",
            "results": []
        })

    all_entries = util.list_entries()

    exact_match = next((entry for entry in all_entries if entry.lower() == query.lower()), None)
    if exact_match:
        return redirect("entry", title=exact_match)
    
    results = [entry for entry in all_entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def create(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        title_exists = util.get_entry(title)

        if not title or not content:
            error_message = "The fields cannot be empty."
            return render(request, "encyclopedia/create.html", {
                "error_message": error_message
            })
        
        if title_exists is not None:
            error_message = "This page already exists."
            return render(request, "encyclopedia/create.html", {
                "error_message": error_message
            })

        util.save_entry(title, content)
        return redirect("entry", title)

    return render(request, "encyclopedia/create.html")

def edit(request, title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def update(request):
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()

        if not title or not content:
            error_message = "The fields cannot be empty."
            return render(request, "encyclopedia/edit.html", {
                "error_message": error_message,
                "title": title,
                "content": content
            })

        util.save_entry(title, content)
        return redirect("entry", title)

    return render(request, "encyclopedia/edit.html")

def randomize(request):
    random_page = random.choice(util.list_entries())
    return redirect(f"/wiki/{random_page}")
