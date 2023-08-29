import pandas as pd
import numpy as np
import torch
from bert_model import BertTextCNN
from MyDataSet import MyDataset
from torch.utils.data import DataLoader
from transformers import BertTokenizer
from sklearn.metrics import accuracy_score
TRAIN_FILE = './data/train_data.csv'
DEV_FILE = './data/dev.csv'
bert_model_name = './rbt3'
max_length = 64
batch_size = 16
num_filter = 256
num_classes = 16
epochs = 10
filter_sizes = [3,4,5]
log_interval = 10
save_path = './checkpoint/bert_model.pt'
lr = 5e-6
device = 'cuda'
class EarlyStopping:
    def __init__(self, patience=10, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.delta = delta
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf

    def __call__(self, val_loss):
        if self.best_score is None:
            self.best_score = val_loss
        elif val_loss < self.best_score + self.delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = val_loss
            self.counter = 0
        if self.verbose:
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
        return self.early_stop
if __name__ == "__main__":
    train_df = pd.read_csv(TRAIN_FILE)
    dev_df = pd.read_csv(DEV_FILE)
    tokenizer = BertTokenizer.from_pretrained(bert_model_name)
    train_dataset = MyDataset(train_df,tokenizer,max_length)
    dev_dataset = MyDataset(dev_df,tokenizer,max_len=max_length)
    train_dataloader = DataLoader(train_dataset,batch_size=batch_size,shuffle=True)
    dev_dataloader = DataLoader(dev_dataset,batch_size=16,shuffle=False)
    model = BertTextCNN(bert_model_name, num_filters=num_filter, filter_sizes=filter_sizes, num_classes=num_classes)
    mode = model.to(device)
    # 定义优化器和损失函数
    early_stopping = EarlyStopping(patience=2, verbose=True)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        batch_idx = 0
        for batch_idx,batch_data in enumerate(train_dataloader):
            input_ids, attention_mask, labels = batch_data
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            labels = labels.to(device)
            # 将数据传入模型进行预测和计算损失
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch_idx % log_interval == 0:
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(input_ids), len(train_dataloader.dataset),
                    100. * batch_idx / len(train_dataloader), loss.item()))
        model.eval()
        y_true,y_pred = [],[]
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
        print(f'Epoch {epoch + 1}: val_acc={acc:.4f}')
        early_stopping(acc)
        if early_stopping.early_stop:
            print("Early stopping")
            break
    torch.save(model.state_dict(), save_path)