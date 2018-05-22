'''
텍스트들에 있는 워드를 카운트하는 함수
'''

from konlpy.tag import Komoran
komoran = Komoran()

import sys

write = sys.stdout.write

# 단어 : 빈도수를 매핑시킬 딕셔너리
nouns_dict = {}

# 파일이름을 얻는 함수.
# 경로/파일명N.txt
def get_file(file_count) :
    file_dir = "results/"
    file_name = "result"
    file_extension = ".txt"

    return file_dir + file_name + str(file_count) + file_extension

# 단어들이 들어오면 딕셔너리에 없는 단어면 새롭게 저장하고 있는 단어면 +1
def save_to_dict(nouns) :
    for noun in nouns :
        if len(noun) < 2 : continue

        if noun in nouns_dict :
            nouns_dict[noun] += 1

        else :
            nouns_dict[noun] = 1

# 완성된 딕셔너리를 파일로 저장
def save_to_result() :
    keys = nouns_dict.keys()
    f = open("nouns_result.txt", "a", encoding='utf-8')
    for key in keys :
        noun, count = key, nouns_dict[key]
        f.write(str(noun) + " : " + str(count) +"\n")
        write(noun + " : " + str(count) + "\n")

    f.close()

# 위 과정들 실행
def run() :
    file_count = 1
    f = open(get_file(file_count), 'r', encoding='utf-8')
    while True:
        line = f.readline()
        if not line :
            f.close()
            file_count += 1
            print("Now File Count :",file_count)
            try :
                f = open(get_file(file_count), 'r', encoding='utf-8')
            except :
                print("======================================== Finish ========================================")
                break

        nouns = komoran.nouns(line)
        save_to_dict(nouns)

    f.close()
    save_to_result()

run()