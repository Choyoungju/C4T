from ner_model import predict
from dataset import load_data
import konlpy
from konlpy.tag import Kkma
import re
import nltk
from collections import defaultdict
import pandas as pd
import csv


class Tag_Mapper():
    def __init__(self,sent):
        self.sent = sent
        
        def AC_mapping(ac_list):
            new_ac_list = []
            family_list = ['엄마','아빠','할머니','할아버지','아이','아들','딸','조부',\
                           '가족','친척','조카','부모님','유아','어머니','아버지','아기','어른']
            couple_list = ['연인','여자친구','여친','남자친구','남친','애인','신랑','부인','여자','남자']
            friend_list = ['여동생','남동생','오빠','형님','형','친구','누나','언니','누나','동생']
            for ac in ac_list:
                words = Kkma().pos(ac)
                for word in words:
                    if (word[1] not in ['NNM','NR','JC']) and (word[0] != '명'):
                        if word[0] in family_list: new_ac_list.append('가족')
                        if word[0] in couple_list: new_ac_list.append('연인')
                        if word[0] in friend_list: new_ac_list.append('친구')
                        if '혼자' in word: new_ac_list.append('혼자')
            return list(set(new_ac_list))

        def PR_mapping(pr_list):
            period = 0
            _pr = ['단기','중기','장기']
            period_str = ''
            for pr in pr_list:
                if '주' in pr and '일' not in pr:
                    p1 = re.compile('\w+주')
                    pr1 = p1.findall(pr)
                    if pr1[0][0] in ['일','1']:
                        period = max(period,7)
                    else:
                        period = max(period,15)
                elif '일' in pr:
                    p1 = re.compile('\d+월')
                    p2 = re.compile('\d+일')
                    pr1= p1.findall(pr)
                    pr2= p2.findall(pr)
                    if len(pr1) == 2:
                        period = max(period,30*(int(pr1[1][:-1])-int(pr1[0][:-1]))-int(pr2[0][:-1])+int(pr2[1][:-1]))
                    elif len(pr2) == 2:
                        period = max(period,int(pr2[1][:-1])-int(pr2[0][:-1])+1)
                    elif len(pr2) == 1:
                        period = max(period,int(pr2[0][:-1]))
                elif '달' in pr:
                    period = max(period,31)
          
                elif '년' in pr and '월' not in pr:
                    period = max(period,365)

            if 0 < period <= 7:
                period_str = _pr[0]
            elif 7 < period <=30:
                period_str = _pr[1]
            elif 30< period:
                period_str = _pr[2]
            return period_str

        def WT_mapping(wt_list):
            new_wt_list = []
            for wt in wt_list:
                words = Kkma().pos(wt)
                for word in words:
                    if word[1] in ['NNM','NR','XR','NNG']:
                        new_wt_list.append(word[0])
            return new_wt_list

        def DT_mapping(dt_list):
            season_list = ['봄','여름','가을','겨울']
            new_dt_list = []
            for dt in dt_list:
                for season in season_list:
                    if season in dt:
                        if season is '봄': new_dt_list+=[3,4,5]
                        if season is '여름': new_dt_list+=[6,7,8]
                        if season is '가을': new_dt_list+=[9,10,11]
                        if season is '겨울': new_dt_list+=[12,1,2]
                    
                if '월' in dt:
                    p = re.compile('\d+월')
                    pr = p.findall(dt)
                    if len(pr) >= 2:
                        pr = [int(d[:-1]) for d in pr]
                        if pr[-1] >= pr[0]:
                            new_dt_list+=list(range(pr[0],pr[-1]+1))
                        else:
                            new_dt_list= new_dt_list+ list(range(pr[0],13)) + list(range(1,pr[-1]+1))
                    elif len(pr) == 1:
                        new_dt_list.append(int(pr[0][:-1]))

            return list(set(new_dt_list))

        def LC_mapping(lc_list):
            lc_dict= defaultdict(lambda: [])
            with open('./data/country_city_map.csv',encoding='utf8') as f:
                reader = list(csv.reader(f))
                for line in reader[1:]:
                    lc_dict[line[1]].append(line[0])
            lc_keys = lc_dict.keys()
            for lc in lc_list:
                for key in lc_keys:
                    if lc in lc_dict[key]:
                        lc_list.remove(lc)
                        lc_list.append(key)
            return list(set(lc_list))
        
        def PU_mapping(pu_list):
            new_pu_list = []
            df = pd.read_csv('./data/PU_list.csv')
            foods = list(df['음식'].dropna())
            cultures = list(df['문화'].dropna())
            rest = list(df['휴양'].dropna())
            activities = list(df['활동'].dropna())
            shopping = list(df['쇼핑'].dropna())
            for pu in pu_list:
                for food in foods:
                    if food in pu: new_pu_list.append('음식');break
                for culture in cultures:
                    if culture in pu: new_pu_list.append('문화');break
                for rs in rest:
                    if rs in pu: new_pu_list.append('휴양');break
                for activity in activities:
                    if activity in pu: new_pu_list.append('활동');break
                for shop in shopping:
                    if shop in pu: new_pu_list.append('쇼핑');break
                
            return list(set(new_pu_list))

        def tag_mapping(tag_dict):
            tag_dict['AC'] = AC_mapping(list(tag_dict['AC']))
            tag_dict['PR'] = PR_mapping(list(tag_dict['PR']))
            tag_dict['PU'] = PU_mapping(list(tag_dict['PU']))
            tag_dict['WT'] = WT_mapping(list(tag_dict['WT']))
            tag_dict['DT'] = DT_mapping(list(tag_dict['DT']))
            tag_dict['LC'] = LC_mapping(list(tag_dict['LC']))
            return tag_dict

        def sent_tag_dict(sent,targets):
            tag_dict = defaultdict(lambda: set())
            word=''
            is_tag = False
            for index in range(len(targets)) :
                if targets[index] is not 'O':
                    word+=sent[index]
                    is_tag = True
                    continue
                if is_tag:
                    if len(word) <= 1: word='';continue          
                    tag_dict[targets[index-len(word)][-2:]].add(word)
                    is_tag = False
                    word=''
            mapped_dict = tag_mapping(tag_dict)
            return mapped_dict
        train_id_data, token_vocab, target_vocab = load_data()
        sent, targets = predict(token_vocab, target_vocab,self.sent)
        self.mapped_dict = sent_tag_dict(sent,targets)
        
    def get_dict(self):
        return self.mapped_dict
    

