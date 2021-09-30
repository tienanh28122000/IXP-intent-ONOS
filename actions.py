import get_intent

def build_waypoint_nip(req):
    result = req.get("queryResult")
    parameters = result.get("parameters") 

    middleboxes = parameters.get("middlebox") 
    target = parameters.get("policy-target")
    origin = parameters.get("origin")
    destination = parameters.get("destination")
    allow = parameters.get("allow")
    block = parameters.get("block")
    qos = parameters.get("qos")
    check_yes = parameters.get("check-yes")
    check_no = parameters.get("check-no")

    if middleboxes or target or origin or destination or allow or block or qos :
        print("args\n target: ", target, "\n origin: ", origin, "\n destination: ", destination, "\n middleboxes: ", middleboxes ,"\n qos: ", qos, "\n allow: ", allow, "\n block:", block)
        intent = 'define intent customIntent:'
        if origin:
            intent = intent + '\n from endpoint("' + origin + '")'
            f = open("intent/origin.txt", "w")
            f.write(origin)
            f.close()
        if destination:
            intent = intent + '\n to endpoint("' + destination + '")'
            f = open("intent/destination.txt", "w")
            f.write(destination)
            f.close()
        for index, mb in enumerate(middleboxes):
            if mb:
                f = open("intent/middleboxes.txt", "w")
                f.write(mb)
                f.close()
                if 'add' not in intent:
                    intent = intent + '\n add '
                intent = intent + 'action("' + mb + '")'

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
        for index, al in enumerate(allow):
            if al:
                if 'allow' not in intent:
                    intent = intent + '\n allow '
                intent = intent + 'trafic("' + al + '")'

                if index != (len(middleboxes) - 1):
                    intent = intent + ', '
        for index, bl in enumerate(block):
            if bl:
                if 'block' not in intent:
                    intent = intent + '\n block '
                intent = intent + 'trafic("' + bl + '")'

                if index != (len(middleboxes) - 1):
                    intent = intent + ', '
        print(intent)
        speech = "The info you gave me generated this program:\n " + intent + "\n Is this what you want?"

    elif check_yes == 'yes' :
        print(check_yes)
        
        speech = "Install intent succesfully!"

    elif check_no == 'no' :
        print(check_no)
        speech = "Please rewrite your intent"

    else:
        speech = "What's your intent?"

    return {
        "fulfillmentText": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "nia"
    }


actions = {
    "input.waypoint": build_waypoint_nip
}
