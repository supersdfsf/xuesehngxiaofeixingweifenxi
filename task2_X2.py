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



#———————————————————————————————————————————————————————————————————————————
#####计算就餐人次#####
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din=df2_din.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_am)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din=df2_din.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("有效就餐的记录为：",len(df2_din))
print("包含的内容为:\n",df2_din['hour'].unique())



#———————————————————————————————————————————————————————————————————————————
#标记工作日和非工作日
workday = pd.bdate_range('4/1/2019', '4/30/2019')#提取四月中所有工作日日期
#print(workday)
df_workday=pd.DataFrame({'workday':workday})
df_workday['day']=df_workday['workday'].dt.day#新增一列赋值为时间中的日
df_workday['Number']=1#将工作日标记成1

#清明节不是工作日
df_workday=df_workday.drop([4],axis=0,inplace=False)
df_workdayy=df_workday.drop(['workday'],axis=1)
print(df_workdayy)

#将工作日和非工作日的标记列并入食堂消费记录表中
df2_day=pd.merge(df2_din,df_workdayy,on='day',how='outer')
df2_day=df2_day.fillna(0)#非工作日标记成0
print(df2_day)
print("包含的内容为:\n",df2_day['hour'].unique())

#———————————————————————————————————————————————————————————————————————————
#提取工作日和非工作日的记录画曲线图

#—————————————————————
#提取工作日的记录
df2_day_work=df2_day.loc[df2_day['Number']==1]
gg=df2_day_work['hour'].value_counts()
gg= gg / len(df_workdayy)
gg=gg.sort_index()
#gg=df2_day_work.groupby(['hour'])
plt.plot(gg, marker='o', mec='r', mfc='w')  
plt.title('工作日食堂就餐时间折线图')
plt.xlabel('时间')
plt.ylabel('数量')
plt.xticks(range(24))  # 设置x刻度
plt.savefig('工作日食堂就餐时间折线图.png')
plt.show()



#—————————————————————
#提取非工作日的记录
df_holiday= 30 - len(df_workdayy)
df2_day_holiday=df2_day.loc[df2_day['Number']==0]
hh=df2_day_holiday['hour'].value_counts()
hh= hh / df_holiday
hh=hh.sort_index()
#gg=df2_day_work.groupby(['hour'])
plt.plot(hh, marker='o', mec='r', mfc='w')  
plt.title('非工作日食堂就餐时间折线图')
plt.xlabel('时间')
plt.ylabel('数量')
plt.xticks(range(24))  # 设置x刻度
plt.savefig('非工作日食堂就餐时间折线图.png')
plt.show()


#———————————————————————————结束————————————————————————————————————————
df1=pd.read_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/data1.csv',encoding='gbk')
#####表格合并#####
all_data = pd.merge(new_df2,df1,left_on ='CardNo',right_on = 'CardNo')
all_data['day']=all_data['Date'].dt.day#新增一列赋值为时间中的日
all_data['hour']=all_data['Date'].dt.hour#新增一列赋值为时间中的小时



#———————————————————————————————————————————————————————————————————————————
#####计算就餐人次#####
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
all_data=all_data.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_am)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
all_data=all_data.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("有效就餐的记录为：",len(all_data))



#———————————————————————————————————————————————————————————————————————————
#标记工作日和非工作日
workdayQ = pd.bdate_range('4/1/2019', '4/30/2019')#提取四月中所有工作日日期
#print(workday)
all_workday=pd.DataFrame({'workday':workdayQ})
all_workday['day']=all_workday['workday'].dt.day#新增一列赋值为时间中的日
all_workday['Number']=1#将工作日标记成1

#清明节不是工作日
all_workday=all_workday.drop([4],axis=0,inplace=False)
all_workdayy=all_workday.drop(['workday'],axis=1)

#将工作日和非工作日的标记列并入食堂消费记录表中
df2_dayQ=pd.merge(all_data,all_workdayy,on='day',how='outer')
df2_dayQ=df2_dayQ.fillna(0)#非工作日标记成0
all_day_work=df2_dayQ.loc[df2_dayQ['Number']==1]
all_day_holiday=df2_dayQ.loc[df2_dayQ['Number']==0]

#工作日
print("工作日\n")
#所有在食堂的消费记录
word = "食堂"
word1="超市"
bool=all_day_work['Dept'].str.contains(word)#将在食堂消费的记录提取出来
bool1=all_day_work['Dept'].str.contains(word1)#将在超市消费的记录提取出来
bool2=all_day_work[ ~ all_day_work['Dept'].str.contains('食堂|超市')]#将在超市食堂之外消费的记录提取出来
df2_din=all_day_work[bool]#食堂消费记录
df2_shop=all_day_work[bool1]#超市消费记录
df2_else=bool2#超市食堂之外消费的记录
#-------------------------------------------
#学生在超市
student_shop_M = df2_shop['Money'].sum() / len(df2_shop['CardNo'].unique())#人均消费金额
student_shop_C= len(df2_shop)#刷卡频次
print("学生超市人均消费金额为:",student_shop_M)
print("学生超市人均刷卡频次为:",student_shop_C)

#学生在食堂
student_din_M = df2_din['Money'].sum() / len(df2_din['CardNo'].unique())#人均消费金额
student_din_C= len(df2_din)#刷卡频次
print("学生食堂人均消费金额为:",student_din_M)
print("学生食堂人均刷卡频次为:",student_din_C)

#学生在其他
student_else_M = df2_else['Money'].sum() / len(df2_else['CardNo'].unique())#人均消费金额
student_else_C= len(df2_else)#刷卡频次
print("学生其他人均消费金额为:",student_else_M)
print("学生其他人均刷卡频次为:",student_else_C)

#______非工作日_____________________________________
print("非工作日\n")

#所有在食堂的消费记录
boolQ=all_day_holiday['Dept'].str.contains(word)#将在食堂消费的记录提取出来
bool1Q=all_day_holiday['Dept'].str.contains(word1)#将在超市消费的记录提取出来
bool2Q=all_day_holiday[ ~ all_day_holiday['Dept'].str.contains('食堂|超市')]#将在超市食堂之外消费的记录提取出来
df2_dinQ=all_day_holiday[boolQ]#食堂消费记录
df2_shopQ=all_day_holiday[bool1Q]#超市消费记录
df2_elseQ=bool2Q#超市食堂之外消费的记录
#-------------------------------------------
#学生在超市
student_shop_MQ = df2_shopQ['Money'].sum() / len(df2_shopQ['CardNo'].unique())#人均消费金额
student_shop_CQ= len(df2_shopQ)#刷卡频次
print("学生超市人均消费金额为:",student_shop_MQ)
print("学生超市人均刷卡频次为:",student_shop_CQ)

#学生在食堂
student_din_MQ = df2_dinQ['Money'].sum() / len(df2_dinQ['CardNo'].unique())#人均消费金额
student_din_CQ= len(df2_dinQ)#刷卡频次
print("学生食堂人均消费金额为:",student_din_MQ)
print("学生食堂人均刷卡频次为:",student_din_CQ)

#学生在其他
student_else_MQ = df2_elseQ['Money'].sum() / len(df2_elseQ['CardNo'].unique())#人均消费金额
student_else_CQ= len(df2_elseQ)#刷卡频次
print("学生其他人均消费金额为:",student_else_MQ)
print("学生其他人均刷卡频次为:",student_else_CQ)

#___________________________________________

