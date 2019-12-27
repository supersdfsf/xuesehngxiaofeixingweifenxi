# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:22:54 2019

@author: lenovo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df1=pd.read_csv('C:/Users/lenovo/.spyder-py3/大学生消费行为分析/项目实操/data1.csv',encoding='gbk')
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
print("数据清洗完成后剩余的有效数据量为：",new_df2.shape)
new_df2.drop('TermSerNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列
new_df2.drop('conOperNo',axis=1,inplace=True)#删除TermSerNo和conOperNo两列



#———————————————————————————————————————————————————————————————————————————
#####表格合并#####
all_data = pd.merge(new_df2,df1,left_on ='CardNo',right_on = 'CardNo')
print(all_data)

#———————————————————————————————————————————————————————————————————————————


#计算刷卡的学生数目
student=len(all_data['CardNo'].unique())
print("18级学生总数为:",student)

#依照卡号进行分组，并计算均值
#student= all_data.groupby(['Major'])#根据校园卡进行分组

#人均刷卡频次=本月刷卡总数/人数
#student_month_count=all_data['CardNo'].value_counts()#学生的本月各学生刷卡频次
Times=len(all_data)#刷卡记录总数
student_month_count= Times / student#人均刷卡频次
print("整体18级学生的本月人均刷卡频次为:",student_month_count)

#人均消费=总消费金额/人数
student_spend=all_data['Money'].sum()#学生本月消费总额
student_e_money= student_spend / student#学生本月人平均消费
print("整体18级学生的本月人均消费为:",student_e_money)


#———————————————————————————————任务3.1开始—————————————————————————————————
#——————————————————————————————————————————————————————————————————————————
#专业&性别
#——————————————————————————————————————————————————————————————————————————


#专业数目
Majors=len(all_data['Major'].unique())
Majors_name=all_data['Major'].unique()
print("18级包含专业数为:",Majors)
print("18级包含的专业为:\n",Majors_name)
'''['18工业设计' '18机械制造' '18计算机应用' 
'18电气自动化' '18国贸实务' '18软件技术' '18宝玉石鉴定'
 '18电子商务' '18模具设计' '18连锁经营' '18旅游管理' 
 '18视觉传播' '18国际金融' '18会计' '18商务英语'
 '18金融管理' '18审计' '18嵌入式技术' '18建筑设计' 
 '18皮具艺术' '18国际商务' '18计算机网络' '18工商企管'
 '18市场营销' '18首饰设计' '18工程造价' '18工业工程'
 '18物流管理' '18商务日语' '18建筑工程' '18艺术设计'
 '18工业机器人' '18社会工作' '18汽车检测' '18市政工程'
 '18酒店管理' '18产品艺术' '18机械制造（学徒）'
 '18动漫设计' '18环境艺术' '18投资与理财']'''


#男女生总数
girls=all_data.loc[all_data['Sex']=='女']
boys=all_data.loc[all_data['Sex']=='男']
print("18级女生总数为：",girls)
print("18级男生总数为：",boys)


#groupby方法
Majors_grouped= all_data.groupby(['Major','Sex'])#根据专业和性别进行分组
Majors_group= all_data.groupby(['Major','Sex','Dept'])#根据专业和性别进行分组


def CardTimes(data):
    students=len(data['CardNo'].unique())#计算学生总数
    Times=len(data)#刷卡记录总数
    s_month_count= Times / students#人均刷卡频次
    #print("本月人均刷卡频次为:",student_month_count)
    return s_month_count

def EPeopleSpend(data):
    students=len(data['CardNo'].unique())#计算学生总数
    student_spend=data['Money'].sum()#学生本月消费总额
    s_e_money= student_spend / students#学生本月人平均消费
    #print("整体18级学生的本月人均消费为:",student_e_money)
    return s_e_money

#——————————————————————————————————————————————————————————————————————————


#各专业、不同性别学生的本月人均刷卡频次和人均消费
staff_C=Majors_grouped.apply(CardTimes)#人均刷卡频次
#staff_C.to_csv('task3_X1.csv',encoding='gbk')
#staff_C.to_csv('各专业、不同性别学生的本月人均刷卡频次.csv',encoding='gbk')

staff_E=Majors_grouped.apply(EPeopleSpend)#人均消费
#staff_E.to_csv('task3_X2.csv',encoding='gbk')
#staff_E.to_csv('各专业、不同性别学生的本月人均消费.csv',encoding='gbk')
'''
#各专业、不同性别学生、不同地点的本月人均刷卡频次和人均消费
staff_C_place=Majors_group.apply(CardTimes)#人均刷卡频次
#staff_C_place.to_csv('task3_X3.csv',encoding='gbk')
staff_C_place.to_csv('各专业、不同性别学生、不同地点的本月人均刷卡频次.csv',encoding='gbk')

staff_E_place=Majors_group.apply(EPeopleSpend)#人均消费
#staff_E_place.to_csv('task3_X4.csv',encoding='gbk')
staff_E_place.to_csv('各专业、不同性别学生、不同地点的本月人均消费.csv',encoding='gbk')
'''

#——————————————————————————————————————————————————————————————————————————
#——————————————————————————————————————————————————————————————————————————
####聚类分析


#提取学生的月刷卡记录作为指标一
student_card=new_df2.groupby(['CardNo']).agg({'PeoNo':'count'})
student_card=student_card.reset_index()

#提取学生的月消费金额作为指标二
student_cost=new_df2.groupby(['CardNo']).agg({'Money':'sum'})
student_cost=student_cost.reset_index()

#学生在各食堂的消费金额
#所有在食堂的消费记录
word = "食堂"
bool=new_df2['Dept'].str.contains(word)#将在食堂消费的记录提取出来
df2_din=new_df2[bool]

student_din=new_df2.groupby(['CardNo']).agg({'Dept':'count','Money':'sum'})

#建立相关变量的dataframe
Students_staff = pd.DataFrame({'CardNo':student_cost['CardNo'],
                      'Allcosttime':student_card['PeoNo'],#总消费次数
                      'AllMoney':student_cost['Money']})


student_din=student_din.rename(columns={'Dept':'DinDept',
                                        'Money':'DinAllMoney'})#在食堂消费次数和总金额
Students_staff=pd.merge(Students_staff,
                        student_din,
                        left_on ='CardNo',
                        right_on ='CardNo',
                        how='outer')

#学生在各食堂的消费金额
student_dincost=new_df2.groupby(['CardNo','Dept']).agg({'CardNo':'count','Money':'sum'})
#按照食堂提取记录

Students_staff=Students_staff.fillna(0)#填充缺失值为0
print(Students_staff.isnull().any())#检查表格数据是否有缺失值


#个人
#早餐平均每餐消费额
#午餐平均每餐消费额
#晚餐平均每餐消费额
#平均每餐消费额
#月食堂消费次数
#月总消费金额


#———————————————————————————————————————————————————————————————————————————
#———————————————————————————————————————————————————————————————————————————
#####提取食堂的早中晚餐记录#####
#nname=df2_din['CardNo'].unique()#获得有效的校园卡卡号
new_df2['day']=new_df2['Date'].dt.day#新增一列赋值为时间中的日
new_df2['hour']=new_df2['Date'].dt.hour#新增一列赋值为时间中的小时

#—————————————————————
df2_din_am =new_df2.loc[(new_df2['hour'] >= 7 ) & (new_df2['hour'] <= 9 )]
print("早上就餐的记录",len(df2_din_am))
#早上就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_am1=df2_din_am.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_am)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_am1=df2_din_am1.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("早上有效就餐的记录为：",len(df2_din_am1))
allcost_am=df2_din_am.groupby(['CardNo']).agg({'Money':'sum'}) / 30#早餐平均每餐消费额
din_times_am = df2_din_am1.groupby(['CardNo']).agg({'CardNo':'count'}) 


new_data= new_df2['CardNo'].unique()
new_data = pd.DataFrame({'CardNo':new_data})
new_data= pd.merge(new_data,din_times_am,left_on ='CardNo',right_on = din_times_am.index,how='outer')
new_data=new_data.drop('CardNo_x',axis=1)
new_data=new_data.rename(columns={'CardNo_y':"早餐平均每餐消费"})


#—————————————————————
df2_din_nm =new_df2.loc[(new_df2['hour']>=11) & (new_df2['hour'] <= 13 )]
print("中午就餐的记录",len(df2_din_nm))
#午餐就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_nm1=df2_din_nm.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_nm)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_nm1=df2_din_nm1.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("中午有效就餐的记录为：",len(df2_din_nm1))
allcost_nm=df2_din_nm.groupby(['CardNo']).agg({'Money':'sum'}) / 30#中餐平均每餐消费额
din_times_nm = df2_din_nm1.groupby(['CardNo']).agg({'CardNo':'count'}) 

new_data= pd.merge(new_data,din_times_nm,left_on ='CardNo',right_on = din_times_nm.index,how='outer')
new_data=new_data.drop('CardNo_x',axis=1)
new_data=new_data.rename(columns={'CardNo_y':"午餐平均每餐消费"})


#—————————————————————
df2_din_pm =new_df2.loc[(new_df2['hour']>=17) & (new_df2['hour'] <= 19 )]
print("晚上就餐的记录",len(df2_din_pm))
#晚餐就餐人数
#第一步：去除“校园卡”，“消费地点”和“消费时间”完全相同的消费记录
df2_din_pm1=df2_din_pm.drop_duplicates(subset=['CardNo','Dept','Date'])
#print(df2_din_pm)

#第二步：去除“校园卡”，“消费地点”，“日”和“小时”完全相同的消费记录
df2_din_pm1=df2_din_pm1.drop_duplicates(subset=['CardNo','Dept','day','hour'])
print("晚上有效就餐的记录为：",len(df2_din_pm1))
allcost_pm=df2_din_pm.groupby(['CardNo']).agg({'Money':'sum'}) / 30#晚餐平均每餐消费额
din_times_pm = df2_din_pm1.groupby(['CardNo']).agg({'CardNo':'count'}) 

new_data= pd.merge(new_data,din_times_pm,left_on ='CardNo',right_on = din_times_pm.index,how='outer')
new_data=new_data.drop('CardNo_x',axis=1)
new_data=new_data.rename(columns={'CardNo_y':"晚餐平均每餐消费"})

new_data=new_data.fillna(0)#填充缺失值为0
new_data['食堂消费次数']= new_data['晚餐平均每餐消费'] + new_data['午餐平均每餐消费'] +new_data['早餐平均每餐消费']
new_data=new_data.drop(['早餐平均每餐消费','午餐平均每餐消费','晚餐平均每餐消费'],axis=1)
#平均每餐消费额
allcost_din=new_df2.groupby(['CardNo']).agg({'Money':'sum'}) / 90#晚餐平均每餐消费额



#建立dataframe
data = pd.merge(new_data,allcost_am,left_on ='CardNo',right_on = allcost_am.index,how='outer')

data=data.rename(columns={'Money':"早餐平均每餐消费额"})
data = pd.merge(data,allcost_nm,left_on ='CardNo',right_on = allcost_nm.index,how='outer')
data=data.rename(columns={'Money':"中餐平均每餐消费额"})
data = pd.merge(data,allcost_pm,left_on ='CardNo',right_on = allcost_pm.index,how='outer')
data=data.rename(columns={'Money':"晚餐平均每餐消费额"})
data = pd.merge(data,student_din,left_on ='CardNo',right_on = student_din.index,how='outer')
data=data.rename(columns={'DinDept':"月食堂消费次数",'DinAllMoney':'食堂消费总金额'})
data = pd.merge(data,allcost_din,left_on ='CardNo',right_on = allcost_din.index,how='outer')
data=data.rename(columns={'Money':"平均每餐消费额"})
data=data.drop(['月食堂消费次数','平均每餐消费额'],axis=1)
data=data.fillna(0)#填充缺失值为0

data1=data

data_mean=data.mean(axis = 0)
data_std=data.std(axis = 0)
data1=(data-data_mean)/data_std

data1=data1.drop('CardNo',axis=1)



#——————————————————————————————————————————————————————————————————————————
#KMeans聚类指标
model=KMeans(n_clusters=3).fit(data1)
aa=model.labels_
aaa=model.cluster_centers_
print(model.cluster_centers_)
# 绘制雷达图
labels = data1.columns#标签 
k = 5#数据个数
plot_data = model.cluster_centers_
color = ['b', 'g', 'r']#指定颜色


angles = np.linspace(0, 2*np.pi, k, endpoint=False)# 闭合
plot_data = np.concatenate((plot_data, plot_data[:,[0]]), axis=1) # 闭合
angles = np.concatenate((angles, [angles[0]])) 
fig = plt.figure()#polar参数
ax = fig.add_subplot(111, polar=True) 
for i in range(len(plot_data)):# 画线
    ax.plot(angles, plot_data[i], 'o-', color = color[i], label = '类别'+str(i), linewidth=0.2)
ax.set_rgrids(np.arange(0.01, 3.5, 0.5), np.arange(-1, 2.5, 0.5), fontproperties="SimHei")
ax.set_thetagrids(angles * 180/np.pi, labels, fontproperties="SimHei")
plt.legend(loc = 4)
plt.savefig('雷达图.png')
plt.show()

#——————————————————————————————————————————————————————————————————————————




