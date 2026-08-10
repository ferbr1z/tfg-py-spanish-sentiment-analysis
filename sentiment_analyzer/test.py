from sentiment_analyzer import sentiment_analyzer, emotion_analyzer
from pysentimiento.preprocessing import preprocess_tweet

preprocess_text = preprocess_tweet("@realDonaldTrump esto es increíbleeeee http://bit.ly #sosunamierda añarako 🤣🤣🤣🤣🤣")

print(preprocess_text)
result = sentiment_analyzer(preprocess_text)
print(result)

result_2 = emotion_analyzer(preprocess_text)
print(result_2)