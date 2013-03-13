from datetime import datetime
import json
from logbook.utils import DATA_PATH

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
