from django.http import HttpResponse

def conferences_index(request):
    return HttpResponse("Hello, world. You're at the conferences index.")

def schools_index(request, conference_slug):
    return HttpResponse("You're looking at the schools index for %s." % conference_slug)

def conference_admin(request, conference_slug):
    return HttpResponse("You're looking at the secretariat admin page for %s." % conference_slug)

def school_admin(request, conference_slug, school_slug):
    return HttpResponse("You're looking at the school registration page for %s." % school_slug)