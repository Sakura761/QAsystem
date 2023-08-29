# -*- coding:utf-8 -*-
import flask
import ahocorasick
from gevent import pywsgi

class NerBaseDict():
    def __init__(self):
        self.load_dict()
        self.dis_tree = self.build_actree(self.dis)
        self.pro_tree = self.build_actree(self.pro)
        self.dru_tree = self.build_actree(self.dru)
        self.fod_tree = self.build_actree(self.fod)
        self.tags = {"dis","sym","fod","pro","dep","dru"}
        self.tag2dict = {"dis":self.dis,"sym":self.sym,"fod":self.fod,"pro":self.pro,"dep":self.dep,"dru":self.dru}
        self.tag2tree = {"dis":self.dis_tree,"fod":self.fod_tree,"pro":self.pro_tree,"dru":self.dru_tree}
    def load_dict(self):
        self.dis = [x.strip() for x in open("./data/entities/diseases.txt",encoding='utf-8').readlines()]
        self.dru = [x.strip() for x in open("./data/entities/drugs.txt",encoding='utf-8').readlines()]
        self.fod = [x.strip() for x in open("./data/entities/foods.txt",encoding='utf-8').readlines()]
        self.pro = [x.strip() for x in open("./data/entities/checks.txt",encoding='utf-8').readlines()]
        self.dep = [x.strip() for x in open("./data/entities/department.txt",encoding='utf-8').readlines()]
        self.sym = [x.strip() for x in open("./data/entities/symptoms.txt",encoding='utf-8').readlines()]

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def rule_match(self, text, type):
        region_wds = []
        for i in self.tag2tree[type].iter(text):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        return [{"word":i,"type":type,"recog_label":"dict"} for i in final_wds]
    def recognize(self, text):
        item = {"string": text, "entities": []}
        entities = []
        for type in {"dis","fod","dru"}:
            entity = self.rule_match(text,type)
            entities.extend(entity)
        item["entities"] = entities
        return item
    def dict_predict(self,texts):
        res = []
        for text in texts:
            ents = self.recognize(text)
            if ents["entities"]:
                res.append(ents)
        return res

if __name__ == '__main__':
    model = NerBaseDict()
    # text_list = ["高血压的症状"]
    # result = model.dict_predict(text_list)
    app = flask.Flask(__name__)
    @app.route("/service/api/dict_ner",methods=["GET","POST"])
    def dict_ner():
        data = {"sucess":0}
        result = []
        text_list = flask.request.get_json()["texts"]
        result = model.dict_predict(text_list)
        data["data"] = result
        data["sucess"] = 1
        return flask.jsonify(data)
    server = pywsgi.WSGIServer(("0.0.0.0",60061), app)
    server.serve_forever()
