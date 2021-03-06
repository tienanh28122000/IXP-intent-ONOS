import numpy as np

import dataset
import model
import config
from keras.preprocessing.text import text_to_word_sequence

train = True
test = True

seq2seq = None


def deanonymize(intent, username, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    intent = intent.replace('@username', username)
    intent = intent.replace('@location', origin, 1) if origin is not None else intent
    intent = intent.replace('@location', destination, 1) if destination is not None else intent

    for target in targets:
        intent = intent.replace('@target', target, 1)

    for mb in middleboxes:
        intent = intent.replace('@middlebox', mb, 1)

    for metric in qos:
        intent = intent.replace('@qos metric', metric['name'], 1)
        intent = intent.replace('@qos constraint', metric['constraint'], 1)
        if metric['constraint'] is not 'none':
            intent = intent.replace('@qos value', metric['value'], 1)

    intent = intent.replace('@hour', start) if start is not None else intent
    intent = intent.replace('@hour', end) if end is not None else intent

    intent = intent.replace('@traffic', allow) if allow is not None else intent
    intent = intent.replace('@traffic', block) if block is not None else intent

    return intent


def anonymize(username, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    entities = '@username '
    entities += '@location ' if origin is not None else ''
    entities += '@location ' if destination is not None else ''

    for target in targets:
        entities += '@target '

    for mb in middleboxes:
        entities += '@middlebox '

    for metric in qos:
        entities += '@qos_metric ' + '@qos_constraint '
        if metric['constraint'] is not 'none':
            entities += '@qos_value'

    entities += '@hour ' if start is not None else ''
    entities += '@hour ' if end is not None else ''

    entities += 'allow @traffic ' if allow is not None else ''
    entities += 'block @traffic ' if block is not None else ''

    return entities.strip()


def predict(username, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    global seq2seq, train, test
    entities=[]
    input_words, output_words = dataset.read()
    seq2seq = model.AttentionSeq2Seq(input_words, output_words)
    tmp = anonymize(username, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    entities.append(text_to_word_sequence(tmp, filters=config.DATASET_FILTERS))
    print('entities:',entities)
    intent = seq2seq.predict(entities) 
    print('intent:', intent)
    result = deanonymize(intent, username, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    print('result:', result)

    return result


def init():
    global seq2seq, train, test
    input_words, output_words = dataset.read()

    # Creating the network model
    seq2seq = model.AttentionSeq2Seq(input_words, output_words)
    if train:
        seq2seq.train()
        train = False

    if test:
        seq2seq.test()


if __name__ == "__main__":
    # init()
    q = [{
        'name': 'bandwidth',
        'constraint': 'equal',
        'value': '95 mbps'
    }]
    predict("haianh", "tienanh-pc", "database", ["clientA"], ["firewall"],q,None,None,None,None)
