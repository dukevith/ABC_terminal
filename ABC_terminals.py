#тут три из A, три из B и два из C
'''
Текст задания:
Транспортный цех объединения обслуживает три филиала А, В и С. 
Грузовики перевозят изделия из А в В и из В в С, возвращаясь затем в А без груза. 
Погрузка в А занимает 20 мин, переезд из А в В длится 30 мин, разгрузка и погрузка в В - 40 мин,
переезд в С - 30 мин, разгрузка в С - 20 мин и переезд в А - 20 мин. 
Если к моменту погрузки в А и В отсутствуют изделия, грузовики уходят дальше по маршруту. 
Изделия в А выпускаются партиями по 1000 шт. через 20 ± 3 мин, в В — такими же партиями через 20 ± 5 мин. 
На линии работает 8 грузовиков, каждый перевозит 1000 изделий. В начальный момент все грузовики находятся в А.
Смоделировать работу транспортного цеха объединения в течение 1000 ч. 
Определить частоту пустых перегонов грузовиков между А и В, В и С и сравнить с характеристиками, 
полученными при равномерном начальном распределении грузовиков между филиалами и операциями.
'''
import numpy as np
import matplotlib.pyplot as plt
import random

t_max=60000 #время работы
num_car=8   #количество машин
    
A_product=0 #количество продуктов на A
B_product=0 #количество продуктов на B
C_product=0 #количество продуктов на C

per=0 #счетчик количества переездов всех машин
per_A_B=0 #количество переездов из A в B
per_B_C=0 #количество переездов из B в С
pusto_counter=0 #количество переездов с пустым кузовом
pusto_A_B=0  #количество пустых переезод из A в B
pusto_B_C=0  #количество пустых переезод из B в C

from_A_to_B=20+30+40  #от A до B с учетом поезди разгрузок и загрузок
from_B_to_C=30+20+40  #от B до C с учетом поезди разгрузок и загрузок
from_C_to_A=20        #от C до A с учетом поезди разгрузок и загрузок

A_terminal=[1,2,3]  #указываем какие машины едут из A
B_terminal=[4,5,6]  #указываем какие машины едут из B
C_terminal=[7,8]    #указываем какие машины едут из C

A_maked_time=[] #времена производства на терминале A
B_maked_time=[] #времена производства на терминале B
A_maked_time.append(random.randrange(0,4))  #произвели первый раз A
B_maked_time.append(random.randrange(0,6))  #произвели первый раз B


'''
Цикл ниже создает времена создания товара с погрешностью, указанной в задании
'''
for t in np.arange(0,t_max):
    errorA=random.randrange(-3,4)  #временные погрешности производства A
    errorB=random.randrange(-5,6)  #временные погрешности производства B

    A_maked_time.append(A_maked_time[-1]+20+errorA)   #новые производства с погрешностью A
    B_maked_time.append(A_maked_time[-1]+20+errorB)   #новые производства с погрешностью B
    
    if A_maked_time[t]>=t_max or B_maked_time[t]>=t_max: #ограничение на указанное время
        break
    




loop_list=[0 for x in range(num_car)]    #для учета времени, доваляемого к проезду за круг (у кажой машины)
Car_position=[1,1,1,2,2,2,3,3] #отслеживание позиции машины (тут надо указать стартовую)
Car_capasity=[0 for x in range(num_car)] #количество товара в кузове


for t in np.arange(0,t_max):
    #ПРОЦЕСС ПРОИЗВОДСТВА ТОВАРА  (отталкиваясь от созданных ранее времен)
    if t in A_maked_time:  #процесс производства на A
        A_product+=1000
    if t in B_maked_time:  #процесс производства на B
        B_product+=1000

    for m in np.arange(0,num_car):  #цикл, для учета всех машин
        if m+1 in A_terminal:  #если стартовая позиция - A
            #цикл проезда машины
            if Car_position[m]==1:
                Car_position[m] = 666 #соответствует в пути из A
                t_take=t #стартовое время
                '''
                Логика следующая:
                1) Если товара больше чем вместимость кузова машины
                    Машина увозит 1000 товара
                    На складе убывает 1000
                2) Если товара на терминале меньше 1000 (меньше чем вместимость кузова)
                    Товара на терминале становится 0
                    Весь груз с терминала загружается в машину
                3) Если товара на терминале нет
                    Машина уезжает с пустым кузовом
                '''
                if A_product>999:
                    Car_capasity[m]+=1000
                    A_product-=1000
                elif 0<A_product<1000:
                    Car_capasity[m]=A_product
                    A_product=0
                elif A_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_A_B+=1


            if t==t_take+from_A_to_B+loop_list[m]:   
                per_A_B+=1
                per+=1
                Car_position[m] = 2 
                B_product+=Car_capasity[m]
                Car_capasity[m]=0

                if B_product>999:
                    Car_capasity[m]+=1000
                    B_product-=1000
                elif 0<B_product<1000:
                    Car_capasity[m]=B_product
                    B_product=0
                elif B_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_B_C+=1

            if t==t_take+from_A_to_B+from_B_to_C+loop_list[m]: 
                per_B_C+=1
                per+=1
                Car_position[m] = 3
                C_product+=Car_capasity[m]
                Car_capasity[m]=0

            if t==t_take+from_A_to_B+from_B_to_C+from_C_to_A+loop_list[m]:
                per+=1
                Car_position[m]=1
                loop+=from_A_to_B+from_B_to_C+from_C_to_A
                loop_list[m]+=loop  #каждый круг добавляется время проезда предыдущих кругов
                loop=0
                
                
        if m+1 in B_terminal: #если стартовая позиция - B
            if Car_position[m]==2:
                Car_position[m] = 666
                t_take2=t
                if B_product>999:
                    Car_capasity[m]+=1000
                    B_product-=1000
                elif 0<B_product<1000:
                    Car_capasity[m]=B_product
                    B_product=0
                elif B_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_B_C+=1

            if t==t_take2+from_B_to_C+loop_list[m]: 
                per_B_C+=1
                per+=1
                Car_position[m] = 3
                C_product+=Car_capasity[m]
                Car_capasity[m]=0       
    

            if t==t_take2+from_B_to_C+from_C_to_A+loop_list[m]:
                per+=1
                Car_position[m] = 1 
                A_product+=Car_capasity[m]
                Car_capasity[m]=0

                if A_product>999:
                    Car_capasity[m]+=1000
                    A_product-=1000
                elif 0<A_product<1000:
                    Car_capasity[m]=A_product
                    A_product=0
                elif A_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_A_B+=1

            if t==t_take2+from_B_to_C+from_C_to_A+from_A_to_B+loop_list[m]:
                per_A_B+=1
                per+=1
                Car_position[m] = 2
                B_product+=Car_capasity[m]
                Car_capasity[m]=0
                loop=from_A_to_B+from_B_to_C+from_C_to_A
                loop_list[m]+=loop
                loop=0
                
        if m+1 in C_terminal:  #если стартовая позиция - C

            if Car_position[m]==3:
                t_take3=t
                Car_capasity[m]=0
                Car_position[m]=666

            if t==t_take3+from_C_to_A+loop_list[m]: 
       
                per+=1
                Car_position[m] = 1 
                A_product+=Car_capasity[m]
                Car_capasity[m]=0

                if A_product>999:
                    Car_capasity[m]+=1000
                    A_product-=1000
                elif 0<A_product<1000:
                    Car_capasity[m]=A_product
                    A_product=0
                elif A_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_A_B+=1

            if t==t_take3+from_C_to_A+from_A_to_B+loop_list[m]: 
                per_A_B+=1
                per+=1
                Car_position[m] = 2 
                B_product+=Car_capasity[m]
                Car_capasity[m]=0

                if B_product>999:
                    Car_capasity[m]+=1000
                    B_product-=1000
                elif 0<B_product<1000:
                    Car_capasity[m]=B_product
                    B_product=0
                elif B_product==0:
                    Car_capasity[m]=0
                    pusto_counter+=1
                    pusto_B_C+=1

            if t==t_take3+from_C_to_A+from_A_to_B+from_B_to_C+loop_list[m]:

                per_B_C+=1
                per+=1
                Car_position[m] = 3
                C_product+=Car_capasity[m]
                Car_capasity[m]=0
                loop=from_A_to_B+from_B_to_C+from_C_to_A
                loop_list[m]+=loop 
                loop=0
                
print(str(len(A_terminal))+' из A, '+str(len(B_terminal))+' из B, '+str(len(C_terminal))+' из C.')
print(' ')
print('Общее количество переездов: '+str(per))
print('Количество поездок с пустым кузовом: '+str(pusto_counter)) 
print('Доля пустых переездов: '+str(pusto_counter/per))
print(' ')
print('Количество переездов из A в B: '+str(per_A_B))
print('Количество поездок с пустым кузовом из A в B: '+str(pusto_A_B)) 
print('Доля пустых переездов из A в B: '+str(pusto_A_B/per_A_B))
print(' ')
print('Количество переездов из B в C: '+str(per_B_C))
print('Количество поездок с пустым кузовом из B в C: '+str(pusto_B_C)) 
print('Доля пустых переездов из B в C: '+str(pusto_B_C/per_B_C))
