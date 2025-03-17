from itertools import product
from random import shuffle
n1,n2,e1,e2,r,k,rr,nn,dd,t1,t2,t3,t4,mx,cl=[],[],[],[],[],[],[],0,0,0,0,0,0,0.6,True
while not str(nn).isdigit() or nn<=0:
    try:
        nn=int(input(f'Введите количество ваших учебников:\n'))
        if nn<=0:
            print('(o_O)')
    except:
        print('(︶︹︺)')
x=[0 for ___ in range(nn)]
a=[' понедельник', 'о вторник',' среду',' четверг',' пятницу',' субботу']
def days():
    o=False
    while o==False:
        print('Введите номера учебников')
        for q in a:
            d=[]
            print(f'    в{q}:')
            while True:
                dd=0
                while not str(dd).isdigit() and dd!='' or int(dd)<=0 or int(dd)>nn:
                    try:
                        dd=input('    ')
                        if dd=='':
                            break
                        if int(dd)>nn or int(dd)<=0:
                            print(f'(o_O)\nНомер не записан')
                    except:
                        print('(︶︹︺)')
                if dd=='':
                    break
                d.append(int(dd))
            r.append(d)
        if len([l for l in r if l])!=0:
            o=True
        else:
            print('(o_O)')
days()
for v in r:
    for w in v:
        rr.append(w)
for j in range(nn):
    st=''
    print(f'Введите размеры {j+1} учебника:\n')
    while not st.isdigit() or t3<=0 or t4<=0 or t1<0 or t2!=1 and t2!=2:
        try:
            hh=(t1:=int(input(f'    количество страниц: ')))+(t2:=int(input(f'    тип обложки:\n     1-мягкая\n     2-твёрдая   ')))*5
            vv=hh*(t3:=int(input(f'    длина(см): ')))*(t4:=int(input(f'    ширина(см): ')))
            vvv=vv*rr.count(j+1)
            x[j]=[vvv,[vv,j+1]]
            if t3<=0 or t4<=0 or t1<0 or t2!=1 and t2!=2:
                print(f'(o_O)\nПопробуйте ещё раз')
            st=''.join([str(t1),str(t2),str(t3),str(t4)])
        except:
            print('(︶︹︺)')
print('')
aa=list(product([0,1], repeat=nn))
shuffle(aa)
for u in range(2**nn):
    aaa=list(aa[u])
    for i in [[aaa[l],x[l][0],x[l][1]] for l in range(nn)]:
        if i[0]==0:
            e1.append([i[1],i[2]])
            e2.append([0,[0,0]])
        else:
            e2.append([i[1],i[2]])
            e1.append([0,[0,0]])
    k.append([e1,e2])
    e1,e2=[],[]
def control():
    global n1,n2,c,mx
    c,cl,rtrue=0,False,[l for l in r if l]
    for s in x:
        c+=s[0]
    cc,Flag=c/len(rtrue),True
    for y in k:
        mx1,mx2=0,0
        for g in range(2):
            summ1=0
            for h in range(len(y[g])):
                summ1+=int(y[g][h][0])
            if g==0:
                summ2,summ1=summ1,0
        p=abs(summ1-summ2)
        print('     ',summ1,summ2)
        for v in r:
            if v:
                for gg in range(2):
                    summd1=0
                    for hh in range(len(y[gg])):
                        summd1+=int(y[gg][hh][1][0]*v.count(y[gg][hh][1][1]))
                    if gg == 0:
                        summd2,summd1=summd1,0
                pd1,pd2=abs(summd1-cc)/cc,abs(summd2-cc)/cc
                if pd1>mx1:
                    mx1=pd1
                if pd2>mx2:
                    mx2=pd2
                if pd1>mx or pd2>mx:
                    flag=False
                    break
                else:
                    flag=True
        if p<c and flag==True:
            c=p
            n1=[i[1][1] for i in y[0] if i[1][1]!=0]
            n2=[i[1][1] for i in y[1] if i[1][1]!=0]
        print(max(mx1,mx2))
    if n1 or n2:
        print(f'\nМинимальная разница в весе = {c},\nсоответствующее распределение: {n1},{n2}')
        print(f'Чтобы изменить максимальное значение для амплитуды весов, введите "амплитуда".\nЧтобы изменить расписание, введите "расписание".')
        ee=input()
        if ee=='амплитуда':
            mx=float(input('Введите новое значение: '))
            cl=True
        control()
        if ee=='расписание':
            days()
            cl=True
    else:
        print(f'\nНе удалось найти подходящее распределение.\nПопробуйте изменить максимальное значение для амплитуды весов или нажмите enter:')
        try:
            mx=float(input())
            fl=True
        except:
            fl=False
        if fl!=False:
            cl=True
        print(f'Чтобы изменить расписание, введите "расписание".')
        ee=input()
        if ee=='расписание':
            days()
            cl=True
if cl==True:
    control()
