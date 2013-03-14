import json
import datetime
import random

def create_records(project):

    random.seed(123)

    end_date = project['last_date']
    n_active_days = project['samples']
    days_active = project['project_length']
    records = []

    # get some text to generate random task descriptions
    import this
    # convert zen of python from ROT13
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i+c)] = chr((i+13) % 26 + c)
    zen_of_python =  "".join([d.get(c, c) for c in this.s])
    zen_lines = zen_of_python.split('\n')

    for x in range (0, n_active_days):
        record = {}

        record['project'] = project['name']

        random_datetime = end_date - datetime.timedelta(days = random.randint(0, days_active))
        record['date'] = random_datetime.strftime("%d.%m.%Y")

        record['p_done'] = random.randint(1,12)

        record['desc'] = zen_lines[random.randint(0, 20)]
        records.append(record)
    return records


if __name__ == '__main__':

    projects = [ 
                    {'name':'GSoC', 'last_date':datetime.datetime(2011, 12,1), 'project_length':100, 'samples':10},
                    {'name':'plos_one_paper', 'last_date':datetime.datetime(2012, 12,1), 'project_length':300, 'samples':30},
                    {'name':'bayes_modelling', 'last_date':datetime.datetime(2013, 1,1), 'project_length':30, 'samples':2}
            ]

    project_records = []
    for project in projects:
        project_records = project_records + create_records(project)
    print json.dumps(project_records)

    fileObj = open(os.path.join(os.getcwd(), 'logbook/data/records.json'), "w")
    json.dump(project_records, fileObj, indent=1)
    fileObj.close()
