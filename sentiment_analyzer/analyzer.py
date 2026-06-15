import os

os.environ["HF_HUB_OFFLINE"] = "1"

from pysentimiento import create_analyzer

sentiment = create_analyzer(task="sentiment", lang="es")
emotion = create_analyzer(task="emotion", lang="es")
def sentiment_analyzer(request):
    result = sentiment.predict(request)
    return result


def emotion_analyzer(request):
    result = emotion.predict(request)
    return result