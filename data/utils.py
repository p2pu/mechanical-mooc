import unicodecsv

def write_to_csv(data, filename):
    """ data should be a list of dicts. All dicts should have the same keys! """
    if len(data) == 0:
        return
    with open(filename, 'w') as f:
        writer = unicodecsv.writer(f)
        writer.writerow(data[0].keys())
        for elem in data:
            writer.writerow(elem.values())
