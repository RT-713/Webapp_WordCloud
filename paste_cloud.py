import MeCab
from wordcloud import WordCloud
from collections import Counter

def paste_cloud(title, paste_data):
    tagger = MeCab.Tagger()

    text = paste_data
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
    wc.to_file('static/' + title + '.png')
    result_path = title + '.png'

    counter = Counter(word_list)
    top_20 = counter.most_common(20)
    print(top_20)

    return result_path

if __name__ == '__main__':
    title = '蜘蛛の糸'
    paste_data = '''ある日の事でございます。御釈迦様は極楽の蓮池のふちを、独りでぶらぶら御歩きになっていらっしゃいました。
    池の中に咲いている蓮の花は、みんな玉のようにまっ白で、そのまん中にある金色の蕊からは、何とも云えない好い匂が、
    絶間なくあたりへ溢れて居ります。極楽は丁度朝なのでございましょう。
    やがて御釈迦様はその池のふちに御佇みになって、水の面を蔽っている蓮の葉の間から、ふと下の容子を御覧になりました。
    この極楽の蓮池の下は、丁度地獄の底に当って居りますから、水晶のような水を透き徹して、三途の河や針の山の景色が、
    丁度覗き眼鏡を見るように、はっきりと見えるのでございます。'''
    paste_cloud(title, paste_data)
