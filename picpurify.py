import requests
import json
from secrets import PICPURIFY_API_KEY


def picPurifyAPI(imageUrl, rule):
    picpurify_url = 'https://www.picpurify.com/analyse/1.1'
    resultRequest = requests.post(picpurify_url,data = {"url_image":imageUrl, "API_KEY":PICPURIFY_API_KEY, "task":rule, "origin_id":"xxxxxxxxx", "reference_id":"yyyyyyyy"})
    parsedResult = (json.loads(resultRequest.content))
    print(parsedResult)

    try:
        final_decision = parsedResult['final_decision']
        confidence_score_decision =  parsedResult['confidence_score_decision']
    except:
        confidence_score_decision =  None
        final_decision = None
    return final_decision,  confidence_score_decision


'''
{'status': 'success', 'confidence_score_decision': 0.99999928474426, 'nb_units': 1, 'task_call': 'weapon_moderation', 'reject_criteria': [], 'performed': ['weapon_moderation'], 'weapon_moderation': {'weapon_content': False, 'compute_time': 0.0358, 'confidence_score': 0.99999928474426}, 'sub_calls': ['weapon_moderation'], 'final_decision': 'OK', 'media': {'url_image': 'http://pbs.twimg.com/media/E47Wu4XWQAEaq4j.jpg', 'file_image': '', 'media_id': '2a5ddff1b39fb0b2d90357ae545ce26d', 'reference_id': 'yyyyyyyy', 'origin_id': 'xxxxxxxxx'}, 'units_consumed': 1, 'total_compute_time': 0.23037195205688}

If --> K0 significa que hay que moderar
'''