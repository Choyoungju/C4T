import random

class Question_Answering():
    qc = 0
    ans = ''
    @classmethod
    def __init__(cls,_dict):
        cls.qc +=1
        def is_enough(_dict):
            del _dict['LC']
            rq_list = []
            enough = False 
            for key in _dict.keys():
                if len(_dict[key]) <= 0:
                    rq_list.append(key)
            if len(rq_list) == 0 : enough = True
            else: enough = False
            print(rq_list)
            return enough,rq_list
            
        def recommendation(_dict):
            return '가지마세요'
        
        def add_answer(tag_list):
            answer=''
            dial_dict = {
                'AC':['누구랑 가세요?','혹시 동행이 있나요?','일행은 누구에요?'],
                'PR':['얼마 동안 가시게요?','며칠 가실 거에요?','몇 박 몇 일로 가실 거에요?'],
                'PU':['여행가서 어떤거 하고 싶으세요?','여행가서 하고 싶은 거 있어요?','여행가면 뭐하고 싶으세요?'],
                'DT':['언제 쯤 가세요?','몇 월에 가세요?','언제 가시는데요?'],
                'WT':['날씨가 따뜻했으면 좋겠어요, 시원했으면 좋겠어요?','어떤 날씨가 좋으세요?','날씨는 어땠으면 좋겠어요?'],
                'MA':[' 그리고 ',' 또 ']
            }
            if len(tag_list) > 2:
                answer = dial_dict[tag_list[0]][random.randint(0,2)]+dial_dict['MA'][random.randint(0,1)]\
                                    +dial_dict[tag_list[1]][random.randint(0,2)]
            else:
                answer = dial_dict[tag_list[0]][random.randint(0,2)]
                
            return answer
        
        enough,rq_list = is_enough(_dict)
        if enough or cls.qc >= 3:#질문수가 3번 이상이 되면 지금 갖고 있는 걸로 추천
            cls.ans = recommendation(_dict)
            cls.qc = 0
        else:
            cls.ans = add_answer(rq_list)
    def get_ans(self):
        return self.ans 