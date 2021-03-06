import os,shutil,re,json,markdown,time

from statistic import*

fileDir = '.'
rMap = {
    '，': ',',
    '、': ',',
    '‘': '\'',
    '’': '\'',
    '。': '.',
    '“': '"',
    '” ': '"',
    '？': '?',
    '！': '!',
    '(': '(',
    ')': ')',
    '；': ';',
    '：': ':',
    '（': '(',
    '）': ')',
    '|<|<': '《',
    '|>|>': '》',
}

def getindex(title):
    res = re.search(r'\d+', title)
    if(res == None):
        sum = 0
        for c in title:
         sum += ord(c)
        return sum
    return int(res.group(0))

def gen_blog():
    # 清空生成的列表页面 以便重新生成
    pages_dir = 'generate_page/'
    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
    os.mkdir(pages_dir)
    left_item_template = ''
    with open('template/_left_item_template.html', 'r', encoding='utf-8') as fr:
        left_item_template = fr.read()
    list_item_template = ''
    with open('template/_list_item_template.html', 'r', encoding='utf-8') as fr:
        list_item_template = fr.read()
    totalWords = 0
    cats = set()
    pages = []
    file_time_map = dict()
    file_time_map_path = 'file_time_map.json'
    if os.path.exists(file_time_map_path):
        with open(file_time_map_path, 'r', encoding='utf-8') as fr:
            file_time_map = json.loads(fr.read())
    for root, dir, files in os.walk('notes'):
        print(root)
        for file in sorted(files, key=lambda f:getindex(f)):
            filename, filetype=os.path.splitext(file)
            full_path = os.path.join(root, file)
            if(full_path).__contains__('katex'):
                continue
            if file.lower() == 'readme.md':
                continue
            if filetype != '.md':
                continue
            mtime = os.stat(full_path).st_mtime
            modified = full_path not in file_time_map or file_time_map[full_path][0] != mtime
            if os.path.exists(full_path.replace('.md','.html')):
                os.remove(full_path.replace('.md','.html'))
            file_content_head = ''
            countWords = 0
            with open(full_path, 'r', encoding='utf-8') as fr:
                content = fr.read()
                for r in rMap:
                    content = content.replace(r, rMap[r])
                countWords = len(content)
                if countWords == 0:
                    content = f'## {filename}\nTODO 完成{filename}\n'
                countWords = len(content)
                with open(full_path, 'w', encoding='utf-8') as fw:
                    fw.write(content)
                file_time_map[full_path] = [os.stat(full_path).st_mtime, countWords]
                content_split = content.split('\n')
                if len(content_split) < 2:
                    file_content_head = ''
                else:
                    file_content_head = markdown.markdown(content_split[1])
                cat = full_path.split('\\')[1]
                cats.add(cat)
                if pages.count('generate_page/generate_page_' + cat + '.html') == 0:
                    pages.append('generate_page/generate_page_' + cat + '.html')
                full_path = full_path.replace('./', '')
                pages.append(full_path)
                content = list_item_template.format(full_path, filename, file_content_head)
                with open('generate_page/generate_page_' + cat + '.html', 'a+', encoding='utf-8') as fw:
                    fw.write(content)
            print('{0} 字数为: {1}'.format(full_path, countWords))
            totalWords += countWords
    print('总字数: {0}'.format(totalWords))
    sorted_cats = [left_item_template.format(pages.index('generate_page/generate_page_' + cat + '.html'), cat.split('.')[1]) for cat in sorted(list(cats), key=lambda cat: int(cat.split('.')[0]))]
    with open('template/_index.html', 'r', encoding='utf-8') as fr:
        content = fr.read()
        content = content.replace('_left_', '\r\n<div class="split"></div>\r\n'.join(sorted_cats)).replace('_v_', str(time.time()))
        with open('resources/pageMap.json', 'w', encoding='utf-8') as fw:
            fw.write(json.dumps(pages,ensure_ascii=False, indent=4))
        with open('index.html', 'w', encoding='utf-8') as fw:
            fw.write(content)
    with open(file_time_map_path, 'w', encoding='utf-8') as fw:
        fw.write(json.dumps(file_time_map, ensure_ascii=False, indent=4))
    # print(json.dumps(pages,ensure_ascii=False, indent=4))

def gen_statistic():
    statistic = Statistic()
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/notes/')
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/task.py')
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/statistic.py')
    statistic.statistic_code_lines('D:/workspace/chrome_extensions/')
    statistic.statistic_code_lines('D:/workspace/ipynb/')
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/template/_index.html')
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/css/main.css')
    statistic.statistic_code_lines('D:/workspace/git/binghong-chen.github.io/js/index.js')
    statistic.statistic_code_lines('D:/share/autodown')
    statistic.statistic_code_lines('D:/share/playmom/src/main/webapp/js/index.js')
    statistic.statistic_code_lines('D:/share/playmom/src/main/webapp/css/main.css')
    statistic.statistic_code_lines('D:/share/playmom/src/main/webapp/index.jsp')
    statistic.statistic_code_lines('D:/share/playmom/src/main/java/')
    statistic.statistic_code_lines('D:/share/__.py')

    
    print('代码总行数: ', sum(statistic.code_lines_map.values()))
    print('各语言代码行数: ', statistic.code_lines_map)
    print('笔记总字数: ', statistic.note_words)

    data = dict()
    if os.path.exists('statistic.json'):
        data = json.loads(statistic.read('statistic.json'))
    date_key = str(datetime.now())[:10]
    data[date_key] = {
        'total_lines': sum(statistic.code_lines_map.values()),
        'code_lines_detail': statistic.code_lines_map,
        'note_words': statistic.note_words,
    }
    statistic.write('statistic.json', json.dumps(data,indent=4))
    print('查看详细记录：', os.path.abspath('statistic.json'))

if __name__ == '__main__':
    gen_blog()
    gen_statistic();