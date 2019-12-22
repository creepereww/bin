#coding:gbk
'''
作者：王冠超
程序目标：获取小说《黎明破晓的街道》里的人物出现频率及人物关系。
'''
import re
import jieba
from collections import Counter

characters = ['渡部','秋叶','有美子','仲西达彦','新谷','妙子','园美','芦原','钉宫真纪子','本条'] #小说里的主要人物
for character in characters:
	jieba.add_word(character)  #加进jieba字典里
#初始化容器分别存储每行的人物名和人物关系
line_names = list()
relationships = {i:dict() for i in characters}
character_attention = list()
#预处理文本并统计人物频率作为节点权重
with open('黎明破晓的街道.txt','r',encoding = 'utf-8')as f:
	for line in f.readlines():
		#找出每行问题中出现的人物名
		tmp_line_names = [word for word in jieba.cut(line) if word in characters]
		character_attention += tmp_line_names
		if len(tmp_line_names) > 1:
			line_names.append(tmp_line_names)
#统计人物出场频率
character_counter = Counter(character_attention)
#统计人物关系（以每行一起出现的次数代表人物关系）
for line in line_names:
	for character1 in line:
		for character2 in line:
			if character1 == character2:
				continue
			if character2 not in relationships[character1]:
				relationships[character1][character2] = 1
			else:
				relationships[character1][character2] += 1
				
#保存结果
with open('node.csv','w') as f:
	f.write('Id,Label,Weight\n')
	for name, times in character_counter.items():
		f.write('{},{},{}\n'.format(name,name,times))

with open('edge.csv','w') as f:
	f.write('Source,Target,Weight,Type\n')
	for name, edges in relationships.items():
		for v,w in edges.items():
			if w>0:
				f.write("{},{},{},{}\n".format(name,v,str(w),'undirected'))
