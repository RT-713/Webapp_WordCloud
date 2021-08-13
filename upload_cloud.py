import MeCab
from wordcloud import WordCloud
from collections import Counter
from matplotlib import pyplot as plt


def upload_cloud(file_path):
    tagger = MeCab.Tagger()

    with open(file_path, mode='r', encoding='utf-8') as f:
        text = f.read()
        tagger.parse('')
        node = tagger.parseToNode(text)
    
    word_list = []
    while node:
        word_type = node.feature.split(',')[0]
        stop_words = ['てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'もの', 'これ', 'さん', 'して', '的', 'ん',\
        'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う', 'それ', 'ここ', 'ちゃん', 'くん', 'ため', '', \
        'て','に','を','は','の', 'が', 'と', 'た', 'し', 'で', 'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', 'れ','さ','なっ']
        if word_type == '名詞' and node.surface not in stop_words:
            word_list.append(node.surface)
        node = node.next
    
    word_chain = ' '.join(word_list)
        
    wc = WordCloud(background_color='white', font_path='/Library/Fonts/Arial Unicode.ttf', width=800, height=800, stopwords=stop_words)
    wc.generate(word_chain)
    wc.to_file(file_path[:-3] + 'png')
    result_path = file_path[7:-3] + 'png'

    counter = Counter(word_list)
    top_20 = counter.most_common(20)
    print(top_20)
    
    return result_path

if __name__ == '__main__':
    upload_cloud('sample_file.txt')
