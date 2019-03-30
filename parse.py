import csv

def parse(filename):
    '''
    takes a filename and returns attribute information and all the data in array of dictionaries
    '''
    data = []

    with open(filename, 'r') as file:
        csv_file = csv.reader(file)
        # skip the first row
        headers = next(csv_file)

        # iterate through rows of actual data
        for row in csv_file:
            data.append(dict(zip(headers, row)))

    return data
