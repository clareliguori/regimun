from django.shortcuts import render_to_response, get_object_or_404
from regimun_app.models import Conference, School

def conferences_index(request):
    all_conferences_list = Conference.objects.all()
    return render_to_response('conferences/index.html', {'conferences_list': all_conferences_list})

def schools_index(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    all_schools_list = conference.school_set.all()
    return render_to_response('conferences/schools/index.html', {'conference' : conference, 'schools_list': all_schools_list})

def conference_admin(request, conference_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    return render_to_response('conferences/secretariat/index.html', {'conference' : conference})

def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_to_response('conferences/schools/school/index.html', {'conference' : conference, 'school' : school})