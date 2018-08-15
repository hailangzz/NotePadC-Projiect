任务描述：
此次任务为，筛选搜索最近一个月内，广东省国际漫游的高端用户：

条件：
1、广东省；
2、月平均话费大于8；
3、国际漫游话费大于0；

目标：
产生广东省高端漫游通话记录表：（temp.ZZ0806_1  字段(PhoneNumber string)）
使用的表：
1.tag_1104_user_building_province
2.tag_1202_arpu
3.tag_1202_myth_fee

ScriptCode:

hive -e"
create tables if not exists temp.ZZ0806_1 as 
select TT.id as PhoneNumber from
(
     select distinct T1.id from tags.tag_1104_user_building_province T1 INNER JOIN 
     select T2.id from 
     (
         select t2.id from tags.tag_1202_arpu t2 INNER JOIN
         select t3.id from tags.tag_1202_myth_fee t3 on
             (t2.id=t3.id and t2.tag_value>8 and t3.tag_value>0 and t2.dated='2018-06' and t3.dated='2018-06'))T2
      on(T1.id=T2.id and T1.tag_value='广东省' and T1.dated='2018-06')
) TT;
"