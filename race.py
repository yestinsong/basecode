#-*-coding:utf-8
import sys
import json
import random

conf_data_str = '{"Germanic": {"constant_append_prompt": ["Germanic women"], "random_append_prompt": ["Diane Kruger", "Claudia Schiffer", "Heidi Klum", "Lena Meyer-Landrut", "Franka Potente", "Diane Keaton", "Alexandra Maria Lara", "Karoline Herfurth", "Anke Engelke", "Nastassja Kinski"]}, "Russian": {"constant_append_prompt": ["Russian women"], "random_append_prompt": ["Natalia Vodianova", "Irina Shayk", "Anna Kournikova", "Daria Strokous", "Yulia Peresild", "Maria Sharapova", "Olesya Sudzilovskaya", "Svetlana Khodchenkova", "Vera Brezhneva", "Ksenia Sobchak"]}, "Celtic": {"constant_append_prompt": ["Celtic women"], "random_append_prompt": ["Saoirse Ronan", "Laura Whitmore", "Jessie Buckley", "Karen Gillan", "Nicola Coughlan", "Katie McGrath", "Evanna Lynch", "Ruth Negga", "Saoirse-Monica Jackson", "Jamie Dornan"]}, "Italian": {"constant_append_prompt": ["Italian women"], "random_append_prompt": ["Monica Bellucci", "Sophia Loren", "Isabella Rossellini", "Caterina Murino", "Valeria Golino", "Sabrina Ferilli", "Ornella Muti", "Asia Argento", "Monica Vitti", "Laura Pausini"]}, "Indian": {"constant_append_prompt": ["Indian women"], "random_append_prompt": ["Aishwarya Rai Bachchan", "Deepika Padukone", "Priyanka Chopra Jonas", "Kareena Kapoor Khan", "Alia Bhatt", "Kajol", "Madhuri Dixit", "Preity Zinta", "Shraddha Kapoor", "Anushka Sharma"]}, "Indonesian": {"constant_append_prompt": ["Indonesian women"], "random_append_prompt": ["Agnez Mo", "Raisa Andriana", "Luna Maya", "Chelsea Islan", "Pevita Pearce", "Laudya Cynthia Bella", "Maia Estianty", "Anggun", "Ayu Ting Ting", "Bunga Citra Lestari"]}, "Chinese": {"constant_append_prompt": ["Chinese women"], "random_append_prompt": ["Fan Bingbing", "Zhang Ziyi", "Liu Yifei (Crystal Liu)", "Yang Mi", "Li Bingbing", "Zhou Xun", "Vicki Zhao", "Angelababy", "Zhao Wei", "Huang Shengyi"]}, "Japanese": {"constant_append_prompt": ["Japanese women"], "random_append_prompt": ["Kiko Mizuhara", "Masami Nagasawa", "Haruka Ayase", "Aoi Miyazaki", "Yukie Nakama", "Maki Horikita", "Ryoko Hirosue", "Kyoko Fukada", "Mao Inoue", "Yui Aragaki"]}, "African_American": {"constant_append_prompt": ["African_American women"], "random_append_prompt": ["Viola Davis",  "Zendaya", "Halle Berry", "Rihanna", "Kerry Washington", "Taraji P. Henson", "Alicia Keys"]}, "Arab": {"constant_append_prompt": ["Arab women"], "random_append_prompt": ["Salma Hayek",  "Eva Longoria", "Jessica Alba", "Ana de la Reguera", "Kate del Castillo", "Michelle Rodriguez", "Barbara Mori", "Maite Perroni"]}, "Persian": {"constant_append_prompt": ["Persian women"], "random_append_prompt": ["Nazanin Boniadi", "Golshifteh Farahani", "Mahlagha Jaberi", "Negin Mirsalehi", "Leila Hatami", "Shermine Shahrivar", "Bahar Soomekh", "Parisa Fitz-Henley", "Pegah Ferydoni", "Sara Nuru"]}, "Jewish": {"constant_append_prompt": ["Jewish women"], "random_append_prompt": ["Natalie Portman", "Mila Kunis", "Scarlett Johansson", "Gal Gadot", "Rachel Weisz", "Bar Refaeli", "Emmy Rossum", "Alyson Hannigan", "Lea Michele", "Kat Dennings"]}}'


class RacePromptUpgrade(object):
    """
        这是一个对prompt优化的人种修改的类型。主要的输入主要有两方面：
        1、提前注册的race json，表决了支持的人种类型（key），固定新增的prompt token（constant_append_prompt），随机新增的prompt token（random_append_prompt）
        2、线上访问的时候输入的基础prompt，以及期待转换的目标race。 
        该函数回基于选择的race，返回修改后的prompt。
    """
    
    def __init__(self):
        self.race_info_index = {}
        
    def load_race_json(self, input_json):
        """
        :input_json 模块依赖的基础配置信息，读取提前注册的race json str。
        """
        
        self.race_info_index = json.loads(input_json)

        
    def get_random_prompt(self,random_prompt_list, seed, token_number = 3):
        """
        基于seed的随机选择token的功能(简单的伪随机)
        :random_prompt_list 随机toke list
        :seed 随机种子
        :token_number 选择的token 数量
        
        :返回以":"分割token str
        
        """
        
        if len(random_prompt_list) <= token_number:
            return ":".join(random_prompt_list)
        
        prompt_list_len = len(random_prompt_list)

        ###处理固定随机/系统随机的类型，并且防止用户seed设置的过小
        valid_seed = pow(prompt_list_len,token_number)
        if seed == 0:
            valid_seed += random.randint(1,10000)
        else :
            valid_seed += abs(seed)

            
        select_prompt_list = []
        for i in range(token_number):
            selected_index = valid_seed % prompt_list_len
            select_prompt_list.append(random_prompt_list[selected_index])
            valid_seed = int(valid_seed / prompt_list_len)
            
        return ":".join(select_prompt_list)
        
          
    def append_race_prompt(self, race_key, seed = 0):
        """
        :race_key 需要转换的目标race类型，注意race_key 需要跟 race_json 中的key名字保持一致
        :seed 当不传递或者设置为0的时候，系统自己随机产生；当为了仿真等应用需要固定seed以对比的时候，可传入一个非0数值，系统按照传入的seed处理随机
        
        系统的整体返回是一个tuple
        0th ele: 表示成功/失败，-1表示失败、其他数值表示成功。
        1th ele：表示失败/成功的富足信息
        2th ele：返回的内容
        """
        
        ret_list = [-1,"", ""]
        
        ##判断race key 是否合法
        if race_key not in self.race_info_index:
            ret_list[0] = -1
            ret_list[1] = "input race not in race_info_index"
            return tuple(ret_list)
        race_info = self.race_info_index[race_key]
    
            
       
        ##构建返回的list，并且将稳定append的token list加进去
        append_list = []
        append_list.extend(race_info["constant_append_prompt"])
        
        ##根据seed选择要随机加入的token
        random_inner_str = self.get_random_prompt(race_info["random_append_prompt"], seed)
        append_list.append("[" + random_inner_str + ":0.4]")
        
        ##整合返回信息
        ret_list[0] = 1
        ret_list[1] = ""
        ret_list[2] = ",".join(append_list)
        
        return tuple(ret_list)
    
    
###demo case
rpu = RacePromptUpgrade()
rpu.load_race_json(conf_data_str)
print(rpu.append_race_prompt("Celtic"))
        
        
        
