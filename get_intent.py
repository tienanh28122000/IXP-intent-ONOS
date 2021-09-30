def get_intent(username, origin, destination, targets, middleboxes, qos, allow, block):
    intent = 'define intent ' + username + 'Intent:'
    if origin:
        intent = intent + '\n from endpoint("' + origin + '")'
    if destination:
        intent = intent + '\n to endpoint("' + destination + '")'

    for index, mb in enumerate(middleboxes):
        if mb:
            if 'add' not in intent:
                intent = intent + '\n add '
            intent = intent + 'middlebox("' + mb + '")'

            if index != (len(middleboxes) - 1):
                intent = intent + ', '

    for index, metric in enumerate(qos):
        if metric and metric['name'] not in intent:
            if 'with' not in intent:
                intent = intent + '\n with '

            intent = intent + metric['name'] + '("' + metric['constraint']
            intent = intent + '","' + metric['value'] + '")' if metric['constraint'] is not 'none' else intent + '")'

            if index != (len(qos) - 1):
                intent = intent + ', '

    if allow:
        if allow not in intent:
            intent = intent + '\n allow trafic("' + allow + '")'
    if block:
        if block not in intent:
            intent = intent + '\n block trafic("' + block + '")'

    return intent