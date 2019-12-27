# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:22:54 2019

@author: lenovo
"""


import pandas as pd
import matplotlib.pyplot as plt

df1=pd.read_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/data1.csv',encoding='gbk')
df2=pd.read_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/data2.csv',encoding='gbk')
print('表格1行列值为：',df1.shape)#查看表格数据共有多少条
print('表格2行列值为：',df2.shape)#查看表格数据共有多少条

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
print("数据清洗完成后剩余的有效数据量为：",new_df2.shape)
new_df2.drop('TermSerNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列
new_df2.drop('conOperNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列
#保存为csv表格
new_df2.to_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/task1_X.csv',encoding='gbk')



#———————————————————————————————————————————————————————————————————————————
#####表格合并#####
all_data = pd.merge(new_df2,df1,left_on ='CardNo',right_on = 'CardNo')
print(len(all_data))
#保存为csv
all_data.to_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/task1_1_X.csv',encoding='gbk')




