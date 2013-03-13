from datetime import datetime
import json
#from sqlalchemy import Table, Column, String, Boolean, DateTime
#from sqlalchemy.orm import mapper
from shorty.utils import url_for, get_random_uid, DATA_PATH  #session, metadata, 

#url_table = Table('urls', metadata,
#    Column('uid', String(140), primary_key=True),
#    Column('target', String(500)),
#    Column('added', DateTime),
#    Column('public', Boolean)
#)

class URL(object):
    #query = session.query_property()

    def __init__(self, target, public=True, uid=None, added=None):
        self.target = target
        self.public = public
        self.added = added or datetime.utcnow()
        if not uid:
            while 1:
                uid = get_random_uid()
                if not URL.query.get(uid):
                    break
        self.uid = uid
        session.add(self)

    @property
    def short_url(self):
        return url_for('link', uid=self.uid, _external=True)

    def __repr__(self):
        return '<URL %r>' % self.uid

def save_entry_form(request):
    file_path = DATA_PATH
    fileObj = open(file_path, "r")
    records = []
    new_record = {}
    entry_names = ['project', 'p_done', 'date', 'desc', 'tags']

    for entry in entry_names:
        value = request.form.get(entry)
        if value:
            new_record[entry] = value

    try:
        records = json.load(fileObj)
    except:
        pass
    fileObj.close()
    fileObj = open(file_path, "w")
    records.append(new_record)
    json.dump(records, fileObj, indent=1)
