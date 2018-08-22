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
            for ac in ac_list:
                words = Kkma().pos(ac)
                for word in words:
                    if (word[1] not in ['NNM','NR','JC']) and (word[0] != '명'):
                        new_ac_list.append(word[0])
            return new_ac_list

        def PR_mapping(pr_list):
            period = 0
            period_str = ''
            for pr in pr_list:
                if '박' in pr:
                    p1 = re.compile('\d+박')
                    p2 = re.compile('\d+일')
                    pr1 = p1.findall(pr)
                    pr2 = p2.findall(pr)
                    if len(pr2) < 1:
                        period = max(period,int(pr1[0][:-1]))
                    else:
                        period = max(period,int(pr2[0][:-1]))
                elif '일' in pr:
                    p1 = re.compile('\d+월')
                    p2 = re.compile('\d+일')
                    pr1= p1.findall(pr)
                    pr2= p2.findall(pr)
                    if len(pr1) == 2:
                        period = max(period,30*(int(pr1[1][:-1])-int(pr1[0][:-1]))-int(pr2[0][:-1])+int(pr2[1][:-1]))
                    elif len(pr2) == 2:
                        period = max(period,int(pr2[1][:-1])-int(pr2[0][:-1])+1)
                elif '년' in pr and '월' not in pr:
                    period = 365

            if 0 < period <= 7:
                period_str = '단기'
            elif 7 < period <=30:
                period_str = '중기'
            else:
                period_str = '장기'

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
                if dt in season_list: new_dt_list.append(dt)
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
            return lc_list
        
        def PU_mapping(pu_list):
            return pu_list

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


if __name__ == '__main__':
    mapp = Tag_Mapper('3박4일 엄마랑 보라카이로 따뜻한 곳으로 8월에 휴가갈거야')
    print(dict(mapp.get_dict()))
 