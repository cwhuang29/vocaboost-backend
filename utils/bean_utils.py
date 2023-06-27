def getProperties(source, *, permissible=None, forbidden=None):
    dc = {}
    for attr in dir(source):
        if attr.startswith('_') or callable(getattr(source, attr)):
            continue
        if forbidden and attr in forbidden:
            continue
        if permissible and attr not in permissible:
            continue
        dc[attr] = getattr(source, attr)
    return dc


def copyProperties(source, target):
    for attr in dir(source):
        if not attr.startswith('_') and not callable(getattr(source, attr)):
            setattr(target, attr, getattr(source, attr))
