import sys
import json
import random


conf_data = '{"Germanic": {"constant_append_prompt": ["Germanic women"], "random_append_prompt": ["Diane Kruger", "Claudia Schiffer", "Heidi Klum", "Lena Meyer-Landrut", "Franka Potente", "Diane Keaton", "Alexandra Maria Lara", "Karoline Herfurth", "Anke Engelke", "Nastassja Kinski"]}, "Russian": {"constant_append_prompt": ["Russian women"], "random_append_prompt": ["Natalia Vodianova", "Irina Shayk", "Anna Kournikova", "Daria Strokous", "Yulia Peresild", "Maria Sharapova", "Olesya Sudzilovskaya", "Svetlana Khodchenkova", "Vera Brezhneva", "Ksenia Sobchak"]}, "Celtic": {"constant_append_prompt": ["Celtic women"], "random_append_prompt": ["Saoirse Ronan", "Laura Whitmore", "Jessie Buckley", "Karen Gillan", "Nicola Coughlan", "Katie McGrath", "Evanna Lynch", "Ruth Negga", "Saoirse-Monica Jackson", "Jamie Dornan"]}, "Italian": {"constant_append_prompt": ["Italian women"], "random_append_prompt": ["Monica Bellucci", "Sophia Loren", "Isabella Rossellini", "Caterina Murino", "Valeria Golino", "Sabrina Ferilli", "Ornella Muti", "Asia Argento", "Monica Vitti", "Laura Pausini"]}, "Indian": {"constant_append_prompt": ["Indian women"], "random_append_prompt": ["Aishwarya Rai Bachchan", "Deepika Padukone", "Priyanka Chopra Jonas", "Kareena Kapoor Khan", "Alia Bhatt", "Kajol", "Madhuri Dixit", "Preity Zinta", "Shraddha Kapoor", "Anushka Sharma"]}, "Indonesian": {"constant_append_prompt": ["Indonesian women"], "random_append_prompt": ["Agnez Mo", "Raisa Andriana", "Luna Maya", "Chelsea Islan", "Pevita Pearce", "Laudya Cynthia Bella", "Maia Estianty", "Anggun", "Ayu Ting Ting", "Bunga Citra Lestari"]}, "Chinese": {"constant_append_prompt": ["Chinese women"], "random_append_prompt": ["Fan Bingbing", "Zhang Ziyi", "Liu Yifei (Crystal Liu)", "Yang Mi", "Li Bingbing", "Zhou Xun", "Vicki Zhao", "Angelababy", "Zhao Wei", "Huang Shengyi"]}, "Japanese": {"constant_append_prompt": ["Japanese women"], "random_append_prompt": ["Kiko Mizuhara", "Masami Nagasawa", "Haruka Ayase", "Aoi Miyazaki", "Yukie Nakama", "Maki Horikita", "Ryoko Hirosue", "Kyoko Fukada", "Mao Inoue", "Yui Aragaki"]}, "African_American": {"constant_append_prompt": ["African_American women"], "random_append_prompt": ["Viola Davis",  "Zendaya", "Halle Berry", "Rihanna", "Kerry Washington", "Taraji P. Henson", "Alicia Keys"]}, "Arab": {"constant_append_prompt": ["Arab women"], "random_append_prompt": ["Salma Hayek",  "Eva Longoria", "Jessica Alba", "Ana de la Reguera", "Kate del Castillo", "Michelle Rodriguez", "Barbara Mori", "Maite Perroni"]}, "Persian": {"constant_append_prompt": ["Persian women"], "random_append_prompt": ["Nazanin Boniadi", "Golshifteh Farahani", "Mahlagha Jaberi", "Negin Mirsalehi", "Leila Hatami", "Shermine Shahrivar", "Bahar Soomekh", "Parisa Fitz-Henley", "Pegah Ferydoni", "Sara Nuru"]}, "Jewish": {"constant_append_prompt": ["Jewish women"], "random_append_prompt": ["Natalie Portman", "Mila Kunis", "Scarlett Johansson", "Gal Gadot", "Rachel Weisz", "Bar Refaeli", "Emmy Rossum", "Alyson Hannigan", "Lea Michele", "Kat Dennings"]}}'

class racePromptUpgrad(object):
    def __init__(self):
        self.race_info_index = {}
        
    def load_race_json(self, input_json):
        self.race_info_index = json.loads(input_json)
        
    def get_random_prompt(self,random_prompt_list, seed, token_number = 3):
        if len(random_prompt_list) <= token_number:
            return ":".join(random_prompt_list)
        
        prompt_list_len = len(random_prompt_list)

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
        
          
    def append_race_prompt(self, input_prompt, race_key, seed = 0):
        
        if race_key not in self.race_info_index:
            return ""
        
        race_info = self.race_info_index[race_key]
        
        input_prompt = input_prompt.strip()
        if len(input_prompt) != 0 and input_prompt[-1] != ',':
            input_prompt = input_prompt + ','
       

        append_list = []
        append_list.extend(race_info["constant_append_prompt"])
        
        
        random_inner_str = self.get_random_prompt(race_info["random_append_prompt"], seed)
        append_list.append("[" + random_inner_str + ":0.4]")
        
        return input_prompt + ",".join(append_list)
    
    

rpu = racePromptUpgrad()
rpu.load_race_json(conf_data)
print(rpu.append_race_prompt("beautiful girl, masterpiece, relax, looking at camera ","Celtic"))
        
        
        
