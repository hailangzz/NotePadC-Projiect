探究深圳的移动用户信息:
1.创建全国用户的基础信息表：temp.ZZ0808_AllCountryUser (字段：PhoneNumber,Sex,Age,UserCity)

hive -e"
create table if not exists temp.ZZ0808_AllCountryUser as 
select T1.id as PhoneNumber,TT.Sex,TT.Age, T1.tag_value as UserCity from tags.tag_1102_owner_city T1 INNER JOIN
(
    select t2.id as PhoneNumber,t2.tag_value as Sex,t3.tag_value as Age 
           from tags.tag_1101_sex t2 INNER JOIN tags.tag_1101_age t3
                on t2.id=t3.id where t2.dt='2018-06' and t3.dt='2018-06'
) TT
ON T1.id=TT.PhoneNumber where T1.dated='2018-06';
"

2.创建深圳用户的基础信息表：temp.ZZ0808_ShenZhenUser (字段：PhoneNumber,Sex,Age,UserCity)
hive -e"
create table if not exists temp.ZZ0808_ShenZhenUser as 
select PhoneNumber,Sex,Age,UserCity from temp.ZZ0808_AllCountryUser where UserCity='广东深圳';
"

3.创建深圳用户的手机品牌信息表：temp.ZZ0808_ShenZhenUserPhoneBrand(字段：PhoneNumber,Sex,Age,PhoneBrand)
hive -e"
create table if not exists temp.ZZ0808_ShenZhenUserPhoneBrand as 
select t1.PhoneNumber,t1.Sex,t1.Age,t2.tag_value as PhoneBrand from temp.ZZ0808_ShenZhenUser t1 
INNER JOIN
tags.tag_1103_brand t2
on t1.PhoneNumber=t2.id where t2.dt='2018-06';
"

4.创建深圳用户的话费账单信息表(最近6个月)：temp.ZZ0808_ShenZhenUserTelePhoneCharge(字段：PhoneNumber,Sex,Age,ARPU)
#广东数据只能使用 bill_basic_info 此表查询···
hive -e"
create table if not exists temp.ZZ0808_ShenZhenUserTelePhoneCharge as 
select t1.PhoneNumber,t1.Sex,t1.Age,T2.ARPU from temp.ZZ0808_ShenZhenUser t1 INNER JOIN 
(select t2.usernumber as PhoneNumber,SUM(t2.arpu) as ARPU from dw_ods.bill_basic_info t2 where t2.ym between 201801 and 201806 and t2.arpu>0 group by t2.usernumber)T2
on t1.PhoneNumber=T2.PhoneNumber;
"

5.创建深圳用户的信用卡账单信息表(最近6个月)：temp.ZZ0808_ShenZhenUserCreditCardBill(字段：PhoneNumber,Sex,Age,CreditCardFee)
hive -e"
create table if not exists temp.ZZ0808_ShenZhenUserCreditCardBill as 
select t1.PhoneNumber,t1.Sex,t1.Age,T2.CreditCardFee from temp.ZZ0808_ShenZhenUser t1 INNER JOIN 
(select t2.mobile as PhoneNumber,SUM(t2.amount) as CreditCardFee from dw_ods.base_a2p_creditcard_bill_detail t2 where t2.year=2018 and (t2.month=02 or t2.month=06 or t2.month=07 ) and t2.amount>0 group by t2.mobile)T2
on t1.PhoneNumber=T2.PhoneNumber;
"
