import json,os
from py2neo import Graph,Node,Relationship
graph = Graph('http://localhost:7474',user='neo4j',password='123456')  #连接neo4j数据库
class MedicalGraph:
    def __init__(self) -> None:
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.root_path = (self.cur_path[:self.cur_path.find("QAsystem")] + "QAsystem/server").replace("\\","/")
        self.data_path = self.root_path+"/data/medical.json"
    def read_nodes(self):
        f = open(self.data_path,encoding="utf-8")
        data = json.load(f)
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        diseases = [] #疾病
        symptoms = []#症状
        disease_infos = []#疾病信息
        # 构建节点实体关系
        rels_not_eat = [] # 疾病－忌吃食物关系
        rels_do_eat = [] # 疾病－宜吃食物关系
        rels_recommend_food = []
        rels_recommend_drug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_symptom = [] #疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_department = [] #　疾病与科室之间的关系
        # count = 1
        for data_json in data:
            # print(count)
            # count += 1
            disease_info = {}
            disease = data_json["name"]
            disease_info["name"] = data_json["name"]
            disease_info["get_way"] = data_json["get_way"]
            disease_info["get_prob"] = data_json["get_prob"]
            disease_info["desc"] = data_json["desc"]
            disease_info["cause"] = data_json["cause"]
            disease_info["prevent"] = data_json["prevent"]
            disease_info["cure_last_time"] = data_json["cure_last_time"]   
            # disease_info["cure_way"] = data_json["cure_way"]
            disease_info["cure_prob"] = data_json["cure_prob"]
            disease_info["easy_get"] = data_json["easy_get"]
            disease_info["cost_money"] = data_json["cost_money"]
            diseases.append(disease)
            disease_infos.append(disease_info)
            if isinstance(data_json["departments"],str):
                departments.append(data_json["departments"])
                rels_department.append((disease,data_json["departments"]))
            else:
                for department in data_json["departments"]:
                    departments.append(department)
                    rels_department.append((disease,department))
            if isinstance(data_json["check"],str):
                checks.append(data_json["check"])
                rels_check.append((disease,data_json["check"]))
            else:
                for check in data_json["check"]:
                    checks.append(check)
                    rels_check.append((disease,check))
            for drug in data_json["common_drug"]:
                drugs.append(drug)
                rels_recommend_drug.append((disease,drug))
            for symptom in data_json["symptoms"]:
                symptoms.append(symptom)
                rels_symptom.append((disease,symptom))
            for food in data_json["do_eat"]:
                foods.append(food)
                rels_do_eat.append((disease,food))
            for food in data_json["not_eat"]:
                foods.append(food)
                rels_not_eat.append((disease,food))
            for food in data_json["recommend"]:
                foods.append(food)
                rels_recommend_food.append((disease,food))
            for complication in data_json["company"]:
                rels_acompany.append((disease,complication))
        self.disease_infos = disease_infos
        self.diseases = diseases
        self.symptoms = set(symptoms)
        self.drugs = set(drugs)
        self.foods = set(foods)
        self.checks = set(checks)
        self.departments = set(departments)
        self.rels_not_eat = rels_not_eat
        self.rels_do_eat = rels_do_eat
        self.rels_recommend_food = rels_recommend_food
        self.rels_recommend_drug = rels_recommend_drug
        self.rels_check = rels_check
        self.rels_symptom = rels_symptom
        self.rels_acompany = rels_acompany
        self.rels_department = rels_department
    def create_node(self,label,node_names):
        count = 0
        for node_name in node_names:
            node = Node(label,name = node_name)
            graph.create(node)
            count += 1
        print(count)
    def create_disease_node(self):
        count = 0
        for disease_info in self.disease_infos:
            node = Node("disease",name = disease_info["name"],desc = disease_info['desc'],cause = disease_info["cause"],prevent = disease_info['prevent']
                        ,get_way = disease_info["get_way"],cure_last_time = disease_info["cure_last_time"],get_prob = disease_info["get_prob"],
                        cure_prob = disease_info["cure_prob"],easy_get = disease_info["easy_get"],cost_money = disease_info["cost_money"])
            graph.create(node)
            count += 1
        print(count)
    def create_common_node(self):
        self.create_node("drug",self.drugs)
        self.create_node("symptom",self.symptoms)
        self.create_node("food",self.foods)
        self.create_node("check",self.checks)
        self.create_node("department",self.departments)
    def create_rels(self):
        self.create_relationship("disease","food",self.rels_do_eat,"do_eat","宜吃")
        self.create_relationship("disease","food",self.rels_not_eat,"not_eat","忌吃")
        self.create_relationship("disease","food",self.rels_recommend_food,"recommend_eat","推荐食谱")
        self.create_relationship("disease","symptom",self.rels_symptom,"has_symptom","症状")
        self.create_relationship("disease","drug",self.rels_recommend_drug,"recommend_drug","推荐用药")
        self.create_relationship("disease","disease",self.rels_acompany,"acompany_with","并发症")
        self.create_relationship("disease","department",self.rels_department,"belongs_to","所属科室")
        self.create_relationship("disease","check",self.rels_check,"need_check","需做检查")
    def create_relationship(self,start_node,end_node,rels,rel_type,rel_name):
        rels = set(rels)
        for rel in rels:
            p = rel[0]
            q = rel[1]
            # 建立关系的语句
            query = "match(p:%s),(q:%s) where p.name = '%s' and q.name = '%s' create (p)-[r:%s{name:'%s'}]->(q)" % (
                start_node,end_node,p,q,rel_type,rel_name
            )
            try:
                #执行cypher语句
                graph.run(query)
                pass
            except Exception as e:
                print(e)
    def export_data(self):
        with open("../data/entites/dieases.txt",'w', encoding='utf-8') as f:
            for disease in self.diseases:
                f.write(disease + "\n")
        with open('../data/entites/drugs.txt','w',encoding='utf-8') as f:
            for drug in self.drugs:
                f.write(drug+ "\n")
        with open('../data/entites/foods.txt','w',encoding='utf-8') as f:
            for food in self.foods:
                f.write(food+"\n")
        with open('../data/entites/checks.txt','w',encoding='utf-8') as f:
            for check in self.checks:
                f.write(check+"\n")
        with open('../data/entites/department.txt','w',encoding='utf-8') as f:
            for department in self.departments:
                f.write(department+"\n")
        with open("../data/entites/symptoms.txt",'w',encoding='utf-8') as f:
            for symptom in self.symptoms:
                f.write(symptom+"\n")
if __name__ == "__main__":
    medical = MedicalGraph()
    medical.read_nodes()
    # medical.export_data()
    with open("../data/userdict.txt","w",encoding='utf-8') as f:
        for drug in medical.drugs:
            f.write(drug + " dru\n")
        for food in medical.foods:
            f.write(food + " fod\n")
        for check in medical.checks:
            f.write(check + " pro\n")
        for department in medical.departments:
            f.write(department + " dep\n")
        for disease in medical.diseases:
            f.write(disease + " dis\n")
        for symptom in medical.symptoms:
            f.write(symptom + " sym\n")
    # drugs = [] # 药品
    # foods = [] #　食物
    # checks = [] # 检查
    # departments = [] #科室
    # diseases = [] #疾病
    # symptoms = []#症状
    medical.create_common_node()
    medical.create_disease_node()
    print("step1:导入图谱节点中")
    medical.create_common_node()
    medical.create_disease_node()
    print("step2:导入图谱边中")  
    medical.create_rels()    
    