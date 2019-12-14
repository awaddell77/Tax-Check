import csv
def dictionarify(x):
    #should produce list of dictionaries from a csv, with the column headers as the keys

    items = r_csv(x)
    #items = item.contents
    crit = items[0]
    results = []
    for i in range(1, len(items)):
        d = dict.fromkeys(crit, 0)
        for i_2 in range(0, len(items[i])):
            d[crit[i_2]] = items[i][i_2]
        results.append(d)
    return results
def r_csv(x, **kwargs):
    res = []
    mode, enc, delim = kwargs.get('mode', 'rt'),kwargs.get('encoding', 'utf-8'), kwargs.get('delim', ',')

    csv_in = open(x, mode, encoding = enc)
    myreader = csv.reader(csv_in, delimiter = delim)
    for row in myreader: res.append(row)
    csv_in.close()
    return res