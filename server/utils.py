import requests,json
from config import *
from py2neo import Graph
graph = Graph("http://127.0.0.1:7474",user="neo4j",password="123456")
def medical_ner(question):
    url = "http://127.0.0.1:60061/service/api/dict_ner"
    data = {"texts":[question]}
    headers = headers = {'Content-Type':'application/json;charset=utf8'}
    response = requests.post(url=url,data=json.dumps(data),headers=headers)
    result = []
    try:
        result = json.loads(response.text)['data'][0]
    except Exception as e:
        print(e)
    print(result)
    #result的形状 {"string": string, "entities": [{"word":,type:""},{"word":,type:""}],"recog_label":"model"}
    return result
def intent_classify(question):
    url = "http://127.0.0.1:60062/service/api/intent_recognize"
    data = {"text":question}
    headers = headers = {'Content-Type':'application/json;charset=utf8'}
    response = requests.post(url=url,data=json.dumps(data),headers=headers)
    result = json.loads(response.text)['data']
    print(result)
    # result的形状{"label":,"confidence":}
    return result
def neo4j_query(query):
    result = ""
    answer = []
    ress = graph.run(query).data()  #list
    data = ""
    if ress:
        for res in ress:
            res = list(res.values())
            answer.extend(res)
        data = "、".join(answer)
    result = data + "\n"
    return result.replace("\t","    ")    
def get_reply_info(intent_res,ner_res):
    if ner_res == [] or intent_res['label'] == '其他':
        return querys_template['unrecognized']
    return querys_template[intent_res['label']]
def get_answer(question):
    intent_res = intent_classify(question)
    ner_res = medical_ner(question)
    reply_info = get_reply_info(intent_res,ner_res)
    ress = []
    if intent_res['label'] == '其他':
        res = reply_info['replay_answer']
        ress.append(res)
    else:
        entities = ner_res['entities']
        for entity in entities:
            word,type = entity['word'],entity['type']
            if type == reply_info['slot_list'][0]:
                query = reply_info['query'].format(word)
                res = reply_info['reply_template'].format(word) + neo4j_query(query)
                ress.append(res)
    if ress == []:
        return [reply_info['deny_response']]
    return ress
def robot_response(question):
    result = get_answer(question)
    return result


    

