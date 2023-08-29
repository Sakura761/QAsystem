import requests
import json
from bs4 import BeautifulSoup
class Spider():
    def __init__(self) -> None:
        self.diseases = []
        self.mp = {"挂什么科":"departments","需做检查":"check","治疗方法":"cure_way","常用药物":"common_drug","一般费用":"cost_money",
                   "传染性":"get_way","治愈周期":"cure_last_time","治愈率":"cure_prob","患病比例":"get_prob","好发人群":"easy_get",
                   "相关症状":"symptoms","相关疾病":"company"}
        self.values1 = {"cost_money","get_way","cure_last_time","cure_prob","get_prob","easy_get","desc","prevent","cause"}
        self.values2 = {"cure_way","departments","check","symptoms","company","do_eat","not_eat","recommend"}
    def parse_html(self,url,uncode="utf-8"):
        html = ""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
                "Connection":"close"
            }
            res = requests.get(url, headers=headers,timeout=10)
            res.encoding = uncode
            html = BeautifulSoup(res.text, "lxml")
            res.close()
        except Exception as e:
            print(e)
        return html

    def spider_main(self):
        for i in range(1,11000):
            disease_url = "http://3g.jib.xywy.com/il_sii_%s.html" % i
            food_url = "http://jib.xywy.com/il_sii/food/%s.htm" % i
            disease = self.basic_info_spider(disease_url)
            if disease == {}:
                continue
            foods = self.food_spider(food_url)
            for key in foods:
                disease[key] = foods[key]
            for key in self.values1:
                if key not in disease:
                    disease[key] = ""
            for key in self.values2:
                if key not in disease:
                    disease[key] = []
            self.diseases.append(disease)
            print(i)
    def basic_info_spider(self,url):
        disease = {}
        html = self.parse_html(url)
        if html.find("em") == None:
            return {}
        name = html.find("em").text   #疾病名称
        disease["name"] = name
        div = html.find("div",class_="Disease-brief")
        desc = div.find("p").text.strip()     #疾病简介
        disease["desc"] = desc
        basic_infos = html.find("div",class_="reach-list")
        clearfixs = basic_infos.find_all("li",class_="clearfix")
        for clearfix in clearfixs:
            if clearfix.find("a") != None:
                continue
            if clearfix.find("div",class_="reach-left fl") == None:
                continue
            key = clearfix.find("div",class_="reach-left fl").text.replace("：","").strip()
            value = clearfix.find("div",class_="reach-right fl").text.strip()
            if "\u2003" in value:
                value = value.split("\u2003")
            if " \xa0" in value:
                value = value.split("\xa0")
                for i in range(0,len(value)):
                    value[i] = value[i].strip()
            disease[self.mp[key]] = value
        medicines = basic_infos.find_all("li",class_="reach-medicine clearfix")
        for medicine in medicines:
            key = medicine.find("div",class_="reach-tableft fl").text.replace("：","").strip()
            value = []
            values = medicine.find_all("a")
            for a in values:
                s = a.text.strip()
                if " " in s:
                    value.append(s.split(" ")[1])
                else:
                    value.append(s)
            disease[self.mp[key]] = value
        ps = html.find("div",id="disease-by").find_all("p")
        cause = ""
        for p in ps:
            cause += p.text
        disease["cause"] = cause
        ps = html.find("div",id="disease-yuf").find_all("p")
        prevent = ""
        for p in ps:
            prevent += p.text
        disease["prevent"] = prevent
        return disease
    
    def food_spider(self, url):
        food = {}
        html = self.parse_html(url,"gbk")
        divs = html.find("div", class_="diet-item none clearfix")
        ps = divs.findAll("p")
        eats = []
        for p in ps:
            eats.append(p.text)
        food["do_eat"] = eats
        divs = html.findAll("div", class_="diet-item none")
        ps = divs[0].findAll("p")
        not_eat = []
        for p in ps:
            not_eat.append(p.text)
        food["not_eat"] = not_eat
        recommend = []
        ps = divs[1].findAll("p")
        for p in ps:
            recommend.append(p.text)
        food["recommend"] = recommend
        return food
    
    def export2file(self,file = '../data/medical.json'):
        with open(file) as f:
            json.dump(self.diseases,f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    spider = Spider()
    spider.spider_main()
    spider.export2file()
