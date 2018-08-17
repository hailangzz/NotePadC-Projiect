a='aa'
b=12
c=[1,2]
print(type(a))
if type(a) is str:
    print(a)

b=(1,)
b=list(b)
print(b,type(b),len(b))
d=list(b)
print(d)
print (type(str(d)))