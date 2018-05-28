from bayes import BayesianFilter
bf = BayesianFilter()

'''bf.fit("여행지 추천 부탁드립니다.", "추천요청")
bf.fit("여행 가고 싶어요.", "추천요청")
bf.fit("배고프다.", "개소리")
bf.fit("해외여행 어디가 좋아요?", "추천요청")
bf.fit("오늘 밥 뭐먹지?", "개소리")
bf.fit("알고리즘 테스트 어렵다", "개소리")
bf.fit("요즘 어떤 여행지가 좋나요?", "추천요청")
bf.fit("어디 여행을 가야 좋을까요?", "추천요청")
bf.fit("오늘 일정이 어떻게 되요?", "개소리")
bf.fit("배고픈데 밥먹으러 가자", "개소리")'''

def load_data_to_texts(filename) :
    f = open(filename, 'r', encoding='utf-8')
    texts = []
    while True :
        line = f.readline()

        if not line:
            break

        if "내공" in line:
            continue

        else :
            texts.append(line.strip())
    f.close()
    return texts

def training(training_datas, label) :
    for training_data in training_datas :
        bf.fit(training_data, label)

travels = load_data_to_texts("travel.txt")
training(travels, "해외여행 추천")

travels = load_data_to_texts("programming.txt")
training(travels, "프로그래밍")

pre, scorelist = bf.predict("나 여행 가고 싶은데 추천좀 해주세요.")
print("테스트 :","나 여행 가고 싶은데 추천좀 해주세요.")
print("결과 =", pre)
print(scorelist)
print()\

pre, scorelist = bf.predict("파이썬 코딩 어떻게 하나요?")
print("테스트 :","파이썬 코딩 어떻게 하나요?")
print("결과 =", pre)
print(scorelist)
print()

pre, scorelist = bf.predict("어디 여행을 가야 좋을까요?")
print("테스트 :","어디 여행을 가야 좋을까요?")
print("결과 =", pre)
print(scorelist)
print()

pre, scorelist = bf.predict("갈만한 곳 추천좀 해줘.")
print("테스트 :","갈만한 곳 추천좀 해줘.")
print("결과 =", pre)
print(scorelist)
print()