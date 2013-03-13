from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound
from shorty.utils import Pagination, render_template, expose, \
     validate_url, url_for #session, 
from shorty.models import URL, save_entry_form

@expose('/')
def new(request):
    error = url = ''
    if request.method == 'POST':
        project = request.form.get('project')
        date = request.form.get('date')
        if not date:
            error = "I'm sorry but entries without date can not be stored"
        if not error:
            if not project:
                project = "Unknown"
            #save entry to records.json here
            save_entry_form(request)
            error = 'Records for Project "' + project + '" have been saved'
            return render_template('new.html', error=error, url=url)
    return render_template('new.html', error=error, url=url)

@expose('/display/<uid>')
def display(request, uid):
    url = URL.query.get(uid)
    if not url:
        raise NotFound()
    return render_template('display.html', url=url)

@expose('/u/<uid>')
def link(request, uid):
    url = URL.query.get(uid)
    if not url:
        raise NotFound()
    return redirect(url.target, 301)

@expose('/list/', defaults={'page': 1})
@expose('/list/<int:page>')
def list(request, page):
    query = URL.query.filter_by(public=True)
    pagination = Pagination(query, 30, page, 'list')
    if pagination.page > 1 and not pagination.entries:
        raise NotFound()
    return render_template('list.html', pagination=pagination)

def not_found(request):
    return render_template('not_found.html')
