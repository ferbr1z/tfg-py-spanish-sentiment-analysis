from sentiment_analyzer import sentiment_analyzer, emotion_analyzer

result = sentiment_analyzer("Paraguay jugo horrible su primer partido, deben despedir a los jugadores")
print(result)

result_2 = emotion_analyzer("Paraguay jugo horrible su primer partido, deben despedir a los jugadores")
print(result_2)