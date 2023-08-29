import torch
from transformers import BertTokenizer
from bert_model import BertTextCNN
import flask
from gevent import pywsgi
class BertModel():
    def __init__(self) -> None:
        self.device = 'cuda'
        self.model_name = './rbt3'
        self.model_path = './checkpoint/bert_model.pt'
        self.label2class = {5: '治疗方法', 15: '其他', 1: '病因', 9: '禁忌', 
                            13: '功效作用', 14: '病情诊断', 12: '医疗费用', 3: '临床表现(病症表现)', 
                            11: '治疗时间', 2: '预防', 0: '定义', 8: '治愈率',
                            6: '所属科室', 10: '化验/体检方案', 7: '传染性', 4: '相关病症'}
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.num_filter = 256
        self.num_classes = 16
        self.max_length = 64
        self.filter_sizes = [3,4,5]
        self.model = BertTextCNN(self.model_name,num_filters=self.num_filter,filter_sizes=self.filter_sizes,num_classes=self.num_classes)
        self.model.load_state_dict(torch.load(self.model_path))
    def predict(self,text):
        input_encoding = self.tokenizer.encode_plus(
        text,
        max_length=self.max_length,
        padding='max_length',
        add_special_tokens=True,
        truncation=True,
        return_tensors='pt'
        )
        self.model = self.model.to(self.device)
        self.model.eval()
        with torch.no_grad():
            input_ids = input_encoding['input_ids']
            input_ids = input_ids.to(self.device)
            attention_mask = input_encoding['attention_mask'].to(self.device)
            output = self.model(input_ids, attention_mask=attention_mask)
        output = torch.softmax(output, dim=1)
        # pred = torch.argmax(output,dim=1)
        prob,pred = torch.max(output,dim=1)
        prob = prob.item()
        pred = pred.item()
        result = {'label':self.label2class[pred],'confidence':prob}
        return result


if __name__ == '__main__':
    app = flask.Flask(__name__)
    model = BertModel()
    @app.route('/service/api/intent_recognize',methods=["GET","POST"])
    def intent_recognize():
        data = {'success':False}
        param = flask.request.get_json()
        text = param['text']
        result = model.predict(text)
        data['data'] = result
        data['success'] = True
        return flask.jsonify(data)
    server = pywsgi.WSGIServer(("0.0.0.0",60062), app)
    server.serve_forever()
