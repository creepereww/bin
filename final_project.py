#coding:gbk
'''
���ߣ����ڳ�
����Ŀ�꣺��ȡС˵�����������Ľֵ�������������Ƶ�ʼ������ϵ��
'''
import re
import jieba
from collections import Counter

characters = ['�ɲ�','��Ҷ','������','��������','�¹�','����','԰��','«ԭ','���������','����'] #С˵�����Ҫ����
for character in characters:
	jieba.add_word(character)  #�ӽ�jieba�ֵ���
#��ʼ�������ֱ�洢ÿ�е��������������ϵ
line_names = list()
relationships = {i:dict() for i in characters}
character_attention = list()
#Ԥ�����ı���ͳ������Ƶ����Ϊ�ڵ�Ȩ��
with open('���������Ľֵ�.txt','r',encoding = 'utf-8')as f:
	for line in f.readlines():
		#�ҳ�ÿ�������г��ֵ�������
		tmp_line_names = [word for word in jieba.cut(line) if word in characters]
		character_attention += tmp_line_names
		if len(tmp_line_names) > 1:
			line_names.append(tmp_line_names)
#ͳ���������Ƶ��
character_counter = Counter(character_attention)
#ͳ�������ϵ����ÿ��һ����ֵĴ������������ϵ��
for line in line_names:
	for character1 in line:
		for character2 in line:
			if character1 == character2:
				continue
			if character2 not in relationships[character1]:
				relationships[character1][character2] = 1
			else:
				relationships[character1][character2] += 1
				
#������
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
