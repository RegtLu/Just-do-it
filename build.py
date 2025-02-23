import json
import os
import re
from bs4 import BeautifulSoup
from langchain.schema import Document


def get_content(file_path:str)->str:

    html=open(file_path,encoding='utf-8').read()
    soup = BeautifulSoup(html, 'lxml')
    title=soup.find("meta", {"name":"description"})['content'].split('-')[0]
    element = soup.find(id='__NEXT_DATA__')
    with open('0.json','w',encoding='utf-8') as f:
        f.write(element.text)
    j = json.load(open('0.json','r',encoding='utf-8'))

    k=j['props']['pageProps']['componentProps']['ebce85a2-47e5-45dd-97f6-dd2d9e347dbf']['props']['datasource']['datasource']['ViewModel']['jsonValue']['value']
    def get_texts(node):
        count=0
        texts = []
        if isinstance(node, dict):
            if 't' in node and node.get('t') == "Text/Title":
                for key, value in node.items():
                    texts.extend(get_texts(value))
                texts.append('\n')
                return texts
            if "t" in node and node.get('t') == "Text/AltTitle":
                count += 1
                if count % 2 == 0:
                    return []
                texts.append('\n\n')
            if (node.get("$type") == "MM.Feature.Vasont.Presentation.Text.String.StringViewModel, MM.Feature.Vasont"
                and "it" in node):
                texts.append(node["it"])
            elif (node.get("$type") == "MM.Feature.Vasont.Presentation.Link.LinkViewModel, MM.Feature.Vasont"
                and "Value" in node):
                texts.append(node["Value"])
            for key, value in node.items():
                texts.extend(get_texts(value))
        elif isinstance(node, list):
            for item in node:
                texts.extend(get_texts(item))
        return texts
    texts = get_texts(k)
    pat=re.compile(r"\n\n\n")
    text=re.subn(pat,"\n\n",''.join(texts))
    return text[0]


def build():
    root_dir = './MSD2'
    documents=[]
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('}.html'):
                file_path = os.path.join(dirpath, filename)
                try:
                    document = Document(
                        page_content=get_content(file_path),
                        metadata={"source": file_path}
                    )
                    documents.append(document)
                except Exception as e:
                    print(e)
                    continue
    return documents
