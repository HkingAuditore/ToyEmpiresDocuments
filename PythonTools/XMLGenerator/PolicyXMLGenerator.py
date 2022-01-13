import os

import pandas as pd
from xml.dom import minidom
import openpyxl

src = r'G:\ToyEmpires\ToyEmpires\ToyEmpires\Assets\Documents\政策设计\政策设计表.xlsx'
df = pd.DataFrame(pd.read_excel(src))
print(df)

xml = minidom.Document()
root = xml.createElement('root')
xml.appendChild(root)

for row in df.itertuples():
    policy = xml.createElement('Policy')
    policy.setAttribute('PID', getattr(row,'PID'))
    policy.setAttribute('Type', "1" if getattr(row,'政策类型') == "经济" else "2")
    policy.setAttribute('Occupancy', str(getattr(row,'政策占用')))

    name = xml.createElement('Name')
    policy.appendChild(name)
    name_text = xml.createTextNode(getattr(row,'政策名'))
    name.appendChild(name_text)

    content = xml.createElement('Content')
    policy.appendChild(content)
    content_text = xml.createTextNode(getattr(row,'政策效果'))
    content.appendChild(content_text)

    root.appendChild(policy)

# 保存
try:
    with open('Output.xml', 'w', encoding='UTF-8') as fh:
        # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
        # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
        xml.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        print('OK')
except Exception as err:
    print('错误：{err}'.format(err=err))

