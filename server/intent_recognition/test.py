from transformers import BertTokenizer
from MyDataSet import MyDataset
from bert_model import BertTextCNN
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
import torch
import pandas as pd
model_name = './rbt3'
num_filter = 256
num_classes = 16
device = 'cuda'
filter_sizes = [3,4,5]
model_path = './checkpoint/bert_model.pt'
tokenizer = BertTokenizer.from_pretrained('./rbt3')
df = pd.read_csv('./data/dev.csv')
dev_dataset = MyDataset(df,tokenizer,64)
dev_dataloader = DataLoader(dev_dataset,batch_size=32)
model = BertTextCNN(model_name,num_filter,filter_sizes,num_classes)
model.load_state_dict(torch.load(model_path))
model = model.to(device)
y_true,y_pred = [],[]
model.eval()
for input_ids, attention_mask, labels in dev_dataloader:
    with torch.no_grad():
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)
        logits = model(input_ids, attention_mask=attention_mask)
    preds = torch.argmax(logits, dim=1)
    y_true += labels.tolist()
    y_pred += preds.tolist()
acc = accuracy_score(y_true, y_pred)
print(f'val_acc={acc:.4f}')
