import matplotlib.pyplot as plt
from wordcloud import WordCloud

meta_text = open("words.txt", "r").read()

wc = WordCloud(
    background_color="white",
    colormap="binary",
    stopwords=[],
    max_words=100,
    width=800,
    height=500,
).generate(meta_text)
plt.figure()
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

wc.to_file("result.jpg")
