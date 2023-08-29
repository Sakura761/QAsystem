querys_template = {
    "定义":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query":"match(n:disease) where n.name = '{}' return n.desc",
        "reply_template":"{}的定义如下",
        "intent_strategy" : "",
        "deny_response":"很抱歉没有理解你的意思呢~"
    },
    "病因": {
        "slot_list" : ["dis"],
        "slot_values":None,
        "query":"match(n:disease) where n.name = '{}' return n.cause",
        "reply_template":"{}的病因如下:\n",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个说法问我"
    },
    "预防":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease) WHERE p.name='{}' RETURN p.prevent",
        "reply_template" : "关于 '{}' 疾病您可以这样预防：\n",
        "ask_template" : "请问您问的是疾病 '{}' 的预防措施吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~"
    },
    "临床表现(病症表现)":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:has_symptom]->(q:symptom) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "'{}' 疾病的病症表现一般是这样的：\n",
        "ask_template" : "您问的是疾病 '{}' 的症状表现吗？",
        "intent_strategy" : "",
        "deny_response":"人类的语言太难了！！"
    },
    "相关病症":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:acompany_with]->(q:disease) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "'{}' 疾病的具有以下并发疾病：\n",
        "ask_template" : "您问的是疾病 '{}' 的并发疾病吗？",
        "intent_strategy" : "",
        "deny_response":"人类的语言太难了！！~"
    },
    "治疗方法":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:recommend_drug]->(q:drug) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "'{}' 疾病的可用的药物有：\n",
        "ask_template" : "您问的是疾病 '{}' 的治疗方法吗？",
        "intent_strategy" : "",
        "deny_response":"没有理解您说的意思哦~"
    },
    "所属科室":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:belongs_to]->(q:department) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "得了 '{}' 可以挂这个科室哦：\n",
        "ask_template" : "您想问的是疾病 '{}' 要挂什么科室吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "传染性":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease) WHERE p.name='{}' RETURN p.easy_get",
        "reply_template" : "'{}' 较为容易感染这些人群：\n",
        "ask_template" : "您想问的是疾病 '{}' 会感染哪些人吗？",
        "intent_strategy" : "",
        "deny_response":"没有理解您说的意思哦~"
    },
    "治愈率":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease) WHERE p.name='{}' RETURN p.cure_prob",
        "reply_template" : "得了'{}' 的治愈率为：",
        "ask_template" : "您想问 '{}' 的治愈率吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "治疗时间":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease) WHERE p.name='{}' RETURN p.cure_last_time",
        "reply_template" : "'{}' 的治疗周期为：",
        "ask_template" : "您想问 '{}' 的治疗周期吗？",
        "intent_strategy" : "",
        "deny_response":"很抱歉没有理解你的意思呢~"
    },
    "化验/体检方案":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:need_check]->(q:check) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "得了 '{}' 需要做以下检查：\n",
        "ask_template" : "您是想问 '{}' 要做什么检查吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "禁忌":{
        "slot_list" : ["dis"],
        "slot_values":None,
        "query" : "MATCH(p:disease)-[r:not_eat]->(q:food) WHERE p.name='{}' RETURN q.name",
        "reply_template" : "得了 '{}' 切记不要吃这些食物哦：\n",
        "ask_template" : "您是想问 '{}' 不可以吃的食物是什么吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~~"
    },
    "功效作用":{
        "slot_list":["dru"],
        "slot_valures":None,
        "query":"match(p:disease)-[r:recommend_drug]->(q:drug) where q.name = '{}' return p.name",
        "reply_template":"{}可以治疗以下这些病\n",
        "ask_template":"您是想问{}的功效吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~~"
    },
    '病情诊断':{
        "slot_list":["sym"],
        "slot_valures":None,
        "query":"match(p:disease)-[r:has_symptom]->(q:symptom) where q.name = '{}' return p.name",
        "reply_template":"可能导致‘{}’这个症状的疾病有\n",
        "ask_template":"您是想问什么病有{}这个症状吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~~"
    },
    '医疗费用':{
        "slot_list":["dis"],
        "slot_valures":None,
        "query":"match(p:disease) where p.name = '{}' return p.cost_money",
        "reply_template":"{}的治疗费用如下\n",
        "ask_template":"您是想问治疗{}的费用吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~~"
    },
    "unrecognized":{
        "slot_values":None,
        "replay_answer" : "非常抱歉，我还不知道如何回答您，我正在努力学习中~",
    }
}