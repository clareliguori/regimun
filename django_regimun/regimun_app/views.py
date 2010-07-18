from django.shortcuts import render_to_response, get_object_or_404
from regimun_app.models import Conference, School

def school_admin(request, conference_slug, school_slug):
    conference = get_object_or_404(Conference, url_name=conference_slug)
    school = get_object_or_404(School, url_name=school_slug)
    return render_to_response('regimun_app/school/index.html', {'conference' : conference, 'school' : school})
