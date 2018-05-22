'''
데이터 분석 코드
1. 딕셔너리 txt 파일로부터 로드
2. 단어의 빈도수 기준으로 딕셔너리 정렬(튜플로 반환됨)
3. 위에서 만든 튜플을 txt 파일로 저장
4. 그래프를 20개 단위로 그리고 파일로 저장
'''

from matplotlib import pyplot as plt
from matplotlib import rc, font_manager
import numpy as np

font_location = "C:/Windows/Fonts/NanumSquareR.ttf"
font_manager.FontProperties(fname=font_location)
rc('font', family="NanumSquare")
font_name = font_manager.FontProperties(fname=font_location).get_name()

# 파일로부터 딕셔너리 불러와서 정렬 후 반환하는 함수
def load_dict() :
    f = open("nouns_result.txt", "r", encoding="utf-8")
    nouns_dict = {}

    while True :
        line = f.readline()

        if not line:
            break

        noun, count = line.split(':')
        nouns_dict[noun] = int(count)

    f.close()
    return sorted(nouns_dict.items(), reverse=True, key = lambda t : t[1])

nouns_dict = load_dict() # 딕셔너리 얻어옴
show_range = 200 # 범위.
#print("Maximum Noun : ", nouns_dict[0][0], "(", nouns_dict[0][1], ")")

#for noun_tuple in nouns_dict[:show_range] :
    #print(noun_tuple)

#그래프 출력 및 저장 함수    
def show_graph() :
    global nouns_dict
    global show_range

    interval = 20

    x = [nouns_dict[i][1] for i in range(show_range)]
    y = [nouns_dict[i][0] for i in range(show_range)]

    for i in range(0, show_range, interval) :
        plt.figure(figsize=(12, 5))
        plt.grid()
        plt.ylim([0, 1800])
        plt.bar(y[i:i+interval], x[i:i+interval], align='center', width=0.5)
        plt.xlabel("Nouns")
        plt.ylabel("Frequency")
        title = "Nouns Ranking :" + str(i+1) + "~" + str(i+interval)
        plt.title(title)

        filename = "graph[" + str(i+1) + "-" + str(i+interval) + "].png"
        plt.savefig("graphs/" + filename, dpi=300)
    plt.show()

# 튜플 저장 함수
def save_to_result(noun_tuples) :
    f = open("anal_result.txt", "a", encoding='utf-8')

    for noun_tuple in noun_tuples :
        print(noun_tuple)
        noun, count = noun_tuple[0], noun_tuple[1]
        f.write(str(noun) + " : " + str(count) +"\n")

    f.close()

# show_range 까지의 튜플들만 파일로 저장
save_to_result(nouns_dict[:show_range])
# 그래프 그리기 및 저장
show_graph()
