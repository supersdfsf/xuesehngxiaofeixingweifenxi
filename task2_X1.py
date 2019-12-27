# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:51:26 2019

@author: pc-11
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei' ## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

df2=pd.read_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/data2.csv',encoding='gbk')
print('表格行列值为：',df2.shape)#查看表格数据共有多少条

#———————————————————————————————————————————————————————————————————————————
######数据预处理————缺失值######


print(df2.isnull().any())#检查表格数据是否有缺失值


#———————————————————————————————————————————————————————————————————————————
######数据预处理————转换日期格式#####


print('进行转换前表的类型为：\n',  df2['Date'].dtypes)
df2['Date'] = pd.to_datetime(df2['Date'])#转换日期格式 
print('进行转换后表的类型为：\n',  df2['Date'].dtypes)


#———————————————————————————————————————————————————————————————————————————
######数据预处理————异常值#####


df2_dec=df2.describe()#对统计字段进行描述统计
print(df2_dec)
#plt.scatter(df2['Index'], df2['Money'])#画图观察消费金额分布
#plt.show()
datetimes=df2
datetimes=datetimes.set_index('Date')#重设索引 将日期定为索引
#locs = datetimes.index.indexer_at_time('00:00:00')#提取特定时间点的消费数据
#print(locs)
start_time = '00:00:00'
end_time = '06:00:00'
locs2 = datetimes.index.indexer_between_time(start_time, 
                                             end_time, 
                                             include_start=True,
                                             include_end=False)
df2_night=datetimes.iloc[locs2]#提取出时间位于凌晨的消费数据
print("消费时间在0点至6点的消费数据量有：",df2_night.shape)
df2_night=df2_night.reset_index()
print("凌晨时间消费的地点为:\n",df2_night['Dept'].unique())
print("凌晨时间消费的地点频次数为:\n",df2_night['Dept'].value_counts())

#提取出在食堂消费的数据
#df2_loc=df2.loc[df2['Dept']=="第一食堂"]
df2_outlier=[]
for i in range(len(df2_night)):#提取出消费地点异常的数据
    word1 = "食堂"
    word2="教学楼"
    word3="基础课部"
    if word1 in df2_night.loc[i,'Dept']:
        df2_outlier.append(df2_night.loc[i,:])
    if word2 in df2_night.loc[i,'Dept']:
        df2_outlier.append(df2_night.loc[i,:])
    if word3 in df2_night.loc[i,'Dept']:
        df2_outlier.append(df2_night.loc[i,:])

df2_outlier=pd.DataFrame(df2_outlier)
print("消费地点异常的数据量有：",df2_outlier.shape)
new_df2 = df2[~ df2['Index'].isin(df2_outlier['Index'])]#在原表中删除异常数据的行
new_df2.drop('TermSerNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列
new_df2.drop('conOperNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列
print("清洗后有效数据量为：",new_df2.shape)
new_df2=new_df2.rename(columns={'Index':'IndexNo'})


#———————————————————————————————————————————————————————————————————————————
#———————————————————————————————————————————————————————————————————————————
#———————————————————————————————————————————————————————————————————————————
#取出在食堂消费的记录

word = "食堂"
bool=new_df2['Dept'].str.contains(word)#将在食堂消费的记录提取出来
df2_din=new_df2[bool]
print(df2_din)
print("包含的消费的地点为:\n",df2_din['Dept'].unique())


#———————————————————————————————————————————————————————————————————————————
#####提取食堂的早中晚餐记录#####
#nname=df2_din['CardNo'].unique()#获得有效的校园卡卡号
df2_din['day']=df2_din['Date'].dt.day#新增一列赋值为时间中的日
df2_din['hour']=df2_din['Date'].dt.hour#新增一列赋值为时间中的小时


df2_din_am =df2_din.loc[(df2_din['hour'] >= 7 ) & (df2_din['hour'] <= 9 )]
print("早上就餐的记录",len(df2_din_am))


df2_din_nm =df2_din.loc[(df2_din['hour']>=11) & (df2_din['hour'] <= 13 )]
print("中午就餐的记录",len(df2_din_nm))

df2_din_pm =df2_din.loc[(df2_din['hour']>=17) & (df2_din['hour'] <= 19 )]
print("晚上就餐的记录",len(df2_din_pm))


#———————————————————————————————————————————————————————————————————————————
#####计算就餐人次#####

#—————————————————————
#早上就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_am=df2_din_am.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_am)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_am=df2_din_am.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("早上有效就餐的记录为：",len(df2_din_am))
print("包含的消费的地点为:\n",df2_din_am['Dept'].unique())


#—————————————————————
#午餐就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_nm=df2_din_nm.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_nm)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_nm=df2_din_nm.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("中午有效就餐的记录为：",len(df2_din_nm))
print("包含的消费的地点为:\n",df2_din_nm['Dept'].unique())


#—————————————————————
#晚餐就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_pm=df2_din_pm.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_pm)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_pm=df2_din_pm.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("晚上有效就餐的记录为：",len(df2_din_pm))
print("包含的消费的地点为:\n",df2_din_pm['Dept'].unique())



#———————————————————————————————————————————————————————————————————————————
#####画出饼图#####


#—————————————————————
#早上
haha1=df2_din_am['Dept'].value_counts()
print("早上各消费的地点频次数为:\n",haha1)
la1=df2_din_am['Dept'].unique()
print("早上包含的消费的地点为:\n",la1)

plt.figure(figsize=(6,6))
patches, l_text, p_text = plt.pie(haha1, 
                                  labels=la1,
                                  labeldistance=1.1, 
                                  autopct='%3.1f%%', 
                                  shadow=False, 
                                  startangle=90, 
                                  pctdistance=0.6)
plt.axis('equal')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.title('各食堂早餐就餐人次饼图')
plt.grid()
plt.savefig('各食堂早餐就餐人次饼图.png')
plt.show()


#—————————————————————
#中午
haha2=df2_din_nm['Dept'].value_counts()
print("中午各消费的地点频次数为:\n",haha2)
la2=df2_din_nm['Dept'].unique()
print("中午包含的消费的地点为:\n",la2)

plt.figure(figsize=(6,6))
patches, l_text, p_text = plt.pie(haha2, 
                                  labels=la2,
                                  labeldistance=1.1, 
                                  autopct='%3.1f%%', 
                                  shadow=False, 
                                  startangle=90, 
                                  pctdistance=0.6)
plt.axis('equal')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.title('各食堂午餐就餐人次饼图')
plt.grid()
plt.savefig('各食堂午餐就餐人次饼图.png')
plt.show()


#—————————————————————
#晚上
haha3=df2_din_pm['Dept'].value_counts()
print("晚上各消费的地点频次数为:\n",haha3)
la3=df2_din_pm['Dept'].unique()
print("晚上包含的消费的地点为:\n",la3)

plt.figure(figsize=(6,6))
patches, l_text, p_text = plt.pie(haha3, 
                                  labels=la3,
                                  labeldistance=1.1, 
                                  autopct='%3.1f%%', 
                                  shadow=False, 
                                  startangle=90, 
                                  pctdistance=0.6)
plt.axis('equal')
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.title('各食堂晚餐就餐人次饼图')
plt.grid()
plt.savefig('各食堂晚餐就餐人次饼图.png')
plt.show()


#———————————————————————————结束————————————————————————————————————————



