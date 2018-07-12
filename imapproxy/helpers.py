""" Methods used by the modules """

def parse_ids(str_ids):
    """ Convert string of ids to a list of ids

        str_ids - ids of format "1:6" or "1,3:5" or "1,4"

    If str_ids = "1:10", return (1,2,3,4,5,6).
    If str_ids = "1,3:5", return (1,3,4,5).
    If str_ids = "1,4", return (1,4).
    """

    ids = []
    raw_ids = str_ids.split(',')

    for s in raw_ids:
        if ':' in s:
            (start, end) = s.split(':')
            print(start, end)
            [ids.append(i) for i in range(int(start), int(end)+1)]
        else:
            ids.append(int(s))

    return ids