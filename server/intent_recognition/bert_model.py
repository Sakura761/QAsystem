import torch
import torch.nn as nn
from transformers import BertModel
class TextCNN(nn.Module):
    def __init__(self, embedding_dim, num_filters, filter_sizes,num_classes):
        '''
        Args:
        embedding_dim: 
        num_filters: number of filter
        filter_sizes: list 
        '''
        super(TextCNN, self).__init__()
        self.convs = nn.ModuleList([
            nn.Conv2d(1, num_filters, (k, embedding_dim)) for k in filter_sizes
        ])
        self.fc = nn.Linear(num_filters * len(filter_sizes), num_classes)

    def forward(self, x):
        x = x.unsqueeze(1)  # 添加通道维度  形状:[batch_size,1,sequence_length,hidden_size]
        x = [nn.functional.relu(conv(x)).squeeze(3) for conv in self.convs]  # 卷积和ReLU shape:[batch_size,num_filters,sequence_length-filter_size+1]
        x = [nn.functional.max_pool1d(i, i.size(2)).squeeze(2) for i in x]  # 最大池化  shape:[batch_size,num_filters]
        x = torch.cat(x, 1) #shape [batch_size,num_filters * len(filter_sizes)]
        x = self.fc(x)
        return x

class BertTextCNN(nn.Module):
    def __init__(self, bert_model_name, num_filters, filter_sizes, num_classes):
        super(BertTextCNN, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.text_cnn = TextCNN(self.bert.config.hidden_size, num_filters, filter_sizes,num_classes)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        text_features = outputs.last_hidden_state     # 获取BERT的最后一层的输出  形状:[batch_size,max_len,hidden_size]
        text_features = self.text_cnn(text_features)  # 使用TextCnn提取特征 shape:[batch_size,num_filters * len(filter_sizes)]
        return text_features