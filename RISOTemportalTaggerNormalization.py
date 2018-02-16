# coding: utf-8

import re
from datetime import datetime

'''
Created on 31/08/2012

@author: Adriano Santos

TODO: Realizar um refectory URGENTE nesta classe. Tudo que foi desenvolvido aqui foi, apenas, para análise da proposta.
'''

'''
Método utilizado normalizar as expressoes no formato
#"from" mes dia, ano "to" mes dia, ano 
Retornando intervalo no formato : Data > X < Data
'''

day_numbers = "(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)"
year = "((?<=\s)\d{4}|^\d{4})"
month = "(january|february|march|april|may|june|july|august|september|october|november|december)"
meses = {'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}


'Lista de Padrões Mapeados para normalização'
__AA_EX = "(" + year + " - " + year + ")" 
__FromMDAToMDA_EX = "(from " + month + " " + day_numbers + ", " + year + " to " + month + " " + day_numbers + ", " + year + ")"
__FromMDToMD_EX = "(from " + month + " " + day_numbers + " to " + month + " " + day_numbers + ")" 
__FromMToM_EX = "(from " + month + " to " + month + ")"
__MD_MD_EX = "(" + month + " " + day_numbers + " *- *" + month + " " + day_numbers + ")"
__MDA_EX = "(" + month + " " + day_numbers + ", *" + year + ")"
__AfterMDA_EX = "(after  " + month + " " + day_numbers + ", *" + year + ")"
__BeforeMDA_EX = "(before " + month + " " + day_numbers + ", *" + year + ")"
__DMA_EX = "(" + day_numbers + " " + month + " " + year + ")" 
__MA_EX = "(" + month + " " + year + ")" 
__MD_EX = "(" + month + " " + day_numbers + ")" 
__DM_EX = "(" + day_numbers  + " " + month+ ")" 
__FromDMUtilDM_EX = "(from " + day_numbers + " " + month + " until " + day_numbers + " " + month + ")"

 
# Normalização de valores
def Normalization(text):
    #Inicia um array com todos os padrões mapeados
    arrayFromEx = [__AA_EX, __FromMDAToMDA_EX, __FromMDToMD_EX, __FromMToM_EX, __FromDMUtilDM_EX, __MD_MD_EX, __MDA_EX, __AfterMDA_EX, __BeforeMDA_EX, __DMA_EX, __MA_EX, __MD_EX, __DM_EX]
    value = None
    for regex in arrayFromEx:
        list = __ExpressionReturn(regex, text)
        if len(list) > 0:
            return __NormalizedValue(regex, list)
            
#GAMBIS    
def __NormalizedValue(regex, found):
    if regex == __FromMDAToMDA_EX:
        return __FromMDAToMDA(found)
    elif regex == __FromMDToMD_EX:
        return __FromMDToMD(found)
    elif regex == __FromMToM_EX:
        return __FromMToM(found)
    elif regex == __FromDMUtilDM_EX:
        return __FromDMUntilDM(found)
    elif regex == __MD_MD_EX:
        return __MD_MD(found)
    elif regex == __MDA_EX:
        return __MDA(found)
    elif regex == __AfterMDA_EX:
        return __AfterMDA(found)
    elif regex == __BeforeMDA_EX:
        return __BeforeMDA(found)
    elif regex == __DMA_EX:
        return __DMA(found)
    elif regex == __MA_EX:
        return __MA(found)
    elif regex == __MD_EX:
        return __MD(found)
    elif regex ==__DM_EX:
        return __DM(found)
    elif regex == __AA_EX:
        return __AA(found)
    
def __FromMDAToMDA(found):
     for risotime in found:
         risotime = risotime.replace('from ', '')
         datas = risotime.split(' to ');
         dt1=datetime.strptime(datas[0], '%B %d, %Y')
         dt2=datetime.strptime(datas[1], '%B %d, %Y')
         a= dt1.strftime('%d-%m-%Y')
         b= dt2.strftime('%d-%m-%Y')
         return a + ' < X < ' + b

def __FromDMUntilDM(found):
    for risotime in found:
         risotime = risotime.replace('from ', '')
         datas = risotime.split(' until ');
         data1 = datas[0].split(' ')
         data2 = datas[1].split(' ')
         return  data1[0] + '-' + meses[data1[1].lower()] + ' < X < ' + data2[0] + '-' + meses[data2[1].lower()]
''
#"from" mes dia "to" mes dia : Data > X < Data -- Pegar ano corrente
def __FromMDToMD(found):
       for risotime in found:
           risotime = risotime.replace('from ', '')
           datas = risotime.split(' to ');
           datas[0] = datas[0] + ano
           datas[1] = datas[1] + ano
           dt1=datetime.strptime(datas[0], '%B %d, %Y')
           dt2=datetime.strptime(datas[1], '%B %d, %Y')
           a= dt1.strftime('%d-%m-%Y')
           b= dt2.strftime('%d-%m-%Y')
           return a + ' < X < ' + b

# Expressões para o padrão mes ano
def __MA(found):
    for risotime in found:
        datas = risotime.split(' ')
        return meses[datas[0].lower()] + '-' + datas[1]

# Expressões para o padrão mes dia
def __MD(found):
    for risotime in found:
        datas = risotime.split(' ')
        return datas[1] + '-' + meses[datas[0].lower()] + '-XXXX' 

# Expressões para o padrão mes dia
def __DM(found):
    for risotime in found:
        datas = risotime.split(' ')
        return datas[0] + '-' + meses[datas[1].lower()] + '-XXXX' 


#"from" mes "to" mes : Data > X < Data -- Pegar ano corrente    
def __FromMToM(found):
       
       hoje = datetime.today()
       ano = str(hoje.year)
       
       for risotime in found:
           risotime = risotime.replace('from ', '')
           datas = risotime.split(' to ');
           
           a = 'xx-' + meses[datas[0].lower()] + '-' + ano
           b = 'xx-' + meses[datas[1].lower()] + '-' +  ano
           return a + ' < X < ' + b

#mes dia - mes dia OU mes dia-mes dia: Data > X < Data -- Pegar ano corrente
def __MD_MD(found):
    
    for risotime in found:
       if (risotime.find(' - ') != -1):
           datas = risotime.split(' - ');
       elif (risotime.find('-') != -1):
           datas = risotime.split('-');
      
       datas[0] = datas[0] + ', ' +  ano
       datas[1] = datas[1] + ', ' +  ano
           
       dt1=datetime.strptime(datas[0], '%B %d, %Y')
       dt2=datetime.strptime(datas[1], '%B %d, %Y')
           
       a= dt1.strftime('%d-%m-%Y')
       b= dt2.strftime('%d-%m-%Y')
           
       return a + ' < X < ' + b

#Formato convencional de data mes dia, ano
def __MDA(found):
    for risotime in found:
        dt=datetime.strptime(risotime, '%B %d, %Y')
        return dt.strftime('%d-%m-%Y')

#Para intervalor anterior aa dada encontrada
def __AfterMDA(found):
    for risotime in found:
        risotime = risotime.replace('after ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        return 'X < ' + dt.strftime('%d-%m-%Y')

#Para intervalor posterior aa dada encontrada
def __BeforeMDA(found):
    for risotime in found:
        risotime = risotime.replace('after ','')
        dt=datetime.strptime(risotime, '%B %d, %Y')
        return 'X < ' + dt.strftime('%d-%m-%Y')

#Para datas no formato dia mes ano
def __DMA(found):
    for risotime in found:
        dt=datetime.strptime(risotime, '%d %B %Y')
        return dt.strftime('%d-%m-%Y')

#Para datas no formato ano - ano OU ano-ano
def __AA(found):
    for risotime in found:
        if (risotime.find(' - ') != -1):
           datas = risotime.split(' - ');
        elif (risotime.find('-') != -1):
           datas = risotime.split('-');
        return datas[0] + ' > X < ' + datas[1]

#Retorna a expressão encontrada
def __ExpressionReturn(expression, text):
    reMDA = expression
    regMDA = re.compile(reMDA, re.IGNORECASE)
    found = regMDA.findall(text)
    return [a[0] for a in found if len(a) > 1]