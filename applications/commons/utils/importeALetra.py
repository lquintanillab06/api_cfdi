import math
from decimal import Decimal #, getcontext

class ImporteALetra():

    __flag = 1
    __numero = 0
    __importe_parcial = 0
    __num = 0
    __num_letra = 0
    __num_letras = 0
    __num_letram = 0
    __num_letradm = 0
    __num_letracm = 0
    __num_letramm = 0
    __num_letradmm = 0

    flag = __flag
    
    @classmethod
    def __unidad(cls, numero):
        amount = math.floor(numero)

        if(amount == 9):
            cls.__num = "NUEVE"
            return cls.__num
        if(amount == 8):
            cls.__num = "OCHO"
            return cls.__num
        if(amount == 7):
            cls.__num = "SIETE"
            return cls.__num
        if(amount == 6):
            cls.__num = "SEIS"
            return cls.__num
        if(amount == 5):
            cls.__num = "CINCO"
            return cls.__num
        if(amount == 4):
            cls.__num = "CUATRO"
            return cls.__num
        if(amount == 3):
            cls.__num = "TRES"
            return cls.__num
        if(amount == 2):
            cls.__num = "DOS"
            return cls.__num
        if(amount == 1 and cls.__flag == 0):
            cls.__num = "UNO"
            return cls.__num
        if(amount == 1 and cls.__flag == 1):
            cls.__num = "UN"
            return cls.__num
        if(amount == 0):
            cls.__num = ""
            return cls.__num 
    
    @classmethod
    def __decena(cls, numero):
        
        if (numero >= 90 and numero < 100):
            cls.__num_letra = "NOVENTA "
            if (numero > 90):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 90)}" 
                return cls.__num_letra
            return cls.__num_letra
      
        if (numero >= 80 and numero < 90):
            cls.__num_letra = "OCHENTA "
            if (numero > 80):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 80)}" 
                return cls.__num_letra
            return cls.__num_letra
        
        if (numero >= 70 and numero < 80):
            cls.__num_letra = "SETENTA "
            if (numero > 70):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 70)}" 
                return cls.__num_letra
            return cls.__num_letra

        if (numero >= 60 and numero < 70):
            cls.__num_letra = "SESENTA "
            if (numero > 60):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 60)}" 
                return cls.__num_letra
            return cls.__num_letra
        
        if (numero >= 50 and numero < 60):
            cls.__num_letra = "CINCUENTA "
            if (numero > 50):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 50)}" 
                return cls.__num_letra
            return cls.__num_letra

        if (numero >= 40 and numero < 50):
            cls.__num_letra = "CUARENTA "
            if (numero > 40):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 40)}" 
                return cls.__num_letra
            return cls.__num_letra

        if (numero >= 30 and numero < 40):
            cls.__num_letra = "TREINTA "
            if (numero > 30):
                cls.__num_letra = f"{cls.__num_letra} Y {cls.__unidad(numero - 30)}" 
                return cls.__num_letra
            return cls.__num_letra
            
        if (numero >= 20 and numero < 30):
            if (numero == 20):
                cls.__num_letra = "VEINTE "
            else:
                cls.__num_letra = f"VEINTI{cls.__unidad(numero - 20)}" 
                return cls.__num_letra
            return cls.__num_letra
       
        if (numero >= 10  and numero <20):
            amount = math.floor(numero)
            if (amount == 10):
                cls.__num_letra = "DIEZ "
            if (amount == 11):
                cls.__num_letra = "ONCE "
            if (amount == 12):
                cls.__num_letra = "DOCE "
            if (amount == 13):
                cls.__num_letra = "TRECE "
            if (amount == 14):
                cls.__num_letra = "CATORCE "
            if (amount == 15):
                cls.__num_letra = "QUINCE "
            if (amount == 16):
                cls.__num_letra = "DIECISEIS "
            if (amount == 17):
                cls.__num_letra = "DIECISIETE "
            if (amount == 18):
                cls.__num_letra = "DIECIOCHO "
            if (amount == 19):
                cls.__num_letra = "DIECINUEVE "

            return cls.__num_letra

        if (numero < 10):
            cls.__num_letra = cls.__unidad(numero)
        return cls.__num_letra
        
    @classmethod
    def __centena(cls, numero):
        
        if (numero >= 100):
           
            if(numero >=900 and numero <1000) :
                cls.__num_letras = "NOVECIENTOS "
                if (numero > 900):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 900)} "
                return cls.__num_letras

            if(numero >=800 and numero <900) :
                cls.__num_letras = "OCHOCIENTOS "
                if (numero > 800):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 800)} "
                return cls.__num_letras
            
            if(numero >=700 and numero <800) :
                cls.__num_letras = "SETECIENTOS "
                if (numero > 700):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 700)} "
                return cls.__num_letras
            
            if(numero >=600 and numero <700) :
                cls.__num_letras = "SEISCIENTOS "
                if (numero > 600):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 600)} "
                return cls.__num_letras
            
            if(numero >=500 and numero <600) :
                cls.__num_letras = "QUINIENTOS "
                if (numero > 500):      
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 500)} "
                return cls.__num_letras

            if(numero >=400 and numero <500) :
                cls.__num_letras = "CUATROCIENTOS "
                if (numero > 400):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 400)} "
                return cls.__num_letras
            
            if(numero >=300 and numero <400) :
                cls.__num_letras = "TRESCIENTOS "
                if (numero > 300):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 300)} "
                return cls.__num_letras
            
            if(numero >=200 and numero <300) :
                cls.__num_letras = "DOSCIENTOS "
                if (numero > 200):
                    cls.__num_letras =f"{cls.__num_letras} {cls.__decena(numero - 200)} "
                return cls.__num_letras

            if(numero >=100 and numero <200) :
                if (numero == 100):
                    cls.__num_letras = "CIEN "
                if (numero > 100):
                    cls.__num_letras =f"CIENTO {cls.__decena(numero - 100)} "
                return cls.__num_letras

        if (numero < 100):
            cls.__num_letras =cls.__decena(numero)
        
        return cls.__num_letras
             
    @classmethod
    def __miles(cls, numero):
      
        if (numero >= 1000 and numero <2000):
            cls.__num_letram = f"MIL {cls.__centena(numero % 1000)}"
            return cls.__num_letram

        if (numero >= 2000 and numero < 10000):
            cls.__num_letram = f"{cls.__unidad(numero/1000)} MIL {cls.__centena(numero % 1000)}"
            return cls.__num_letram

        if (numero < 1000):
            cls.__num_letram = cls.__centena(numero)
            return cls.__num_letram

    @classmethod
    def __decmiles(cls, numero):
        if (numero == 10000):
            cls.__num_letradm = "DIEZ MIL"
            return cls.__num_letradm

        if (numero > 10000 and numero <20000):
            cls.__num_letradm =  f"{cls.__decena(numero/1000)} MIL {cls.__centena(numero%1000)}"
            return cls.__num_letradm

        if (numero >= 20000 and numero <100000):
            cls.__num_letradm = f"{cls.__decena(numero/1000)} MIL {cls.__miles(numero%1000)}"
            return cls.__num_letradm
        

        if (numero < 10000):
            cls.__num_letradm = cls.__miles(numero)
            return cls.__num_letradm

    @classmethod
    def __cienmiles(cls, numero):

        if (numero == 100000):
            cls.__num_letracm = "CIEN MIL"
            return cls.__num_letracm

        if (numero >= 100000 and numero <1000000):
            cls.__num_letracm = f"{cls.__centena(numero/1000)} MIL {cls.__centena(numero%1000)}" 
            return cls.__num_letracm
        
        if (numero < 100000):
            cls.__num_letracm = cls.__decmiles(numero)
            return cls.__num_letracm

    @classmethod
    def __millon(cls, numero):
        if (numero >= 1000000 and numero < 2000000):
            cls.__num_letramm = f"UN MILLON {cls.__cienmiles(numero%1000000)}" 
            return cls.__num_letramm

        if (numero >= 2000000 and numero <10000000):
            cls.__num_letramm =  f"{cls.__unidad(numero/1000000)} MILLONES {cls.__cienmiles(numero%1000000)}" 
            return cls.__num_letramm

        if(numero < 1000000):
            cls.__num_letramm = cls.__cienmiles(numero)
            return cls.__num_letramm

    @classmethod
    def __decmillon(cls, numero):
        if (numero == 10000000):
            cls.__num_letradmm = "DIEZ MILLONES"
            return cls.__num_letradmm

        if (numero > 10000000 and numero <20000000):
            cls.__num_letradmm = f"{cls.__decena(numero/1000000)} MILLONES {cls.__cienmiles(numero%1000000)} "  
            return cls.__num_letradmm

        if (numero >= 20000000 and numero <100000000):     
            cls.__num_letradmm = f"{cls.__decena(numero/1000000)} MILLONES {cls.__millon(numero%1000000)} " 
            return cls.__num_letradmm

        if (numero < 10000000):
            cls.__num_letradmm = cls.__millon(numero)
            return cls.__num_letradmm
        

    @classmethod 
    def convertirALetras(cls,numero):
        #getcontext().prec = 2
        numeroInt = math.floor(numero)
        numeroDec =  (Decimal(numero) - Decimal(numeroInt)) *100
        num = cls.__decmillon(numeroInt)
        if (numero % 1000000 == 0.00): 
             return f"{num}DE PESOS {round(numeroDec,0)}/100 M.N"
        else:
            return f"{num}PESOS {round(numeroDec,0)}/100 M.N"
           
            
    @classmethod 
    def convertirALetrasDolares(cls,numero):
        #getcontext().prec = 2
        numeroInt = math.floor(numero)
        numeroDec =  (Decimal(numero) - Decimal(numeroInt)) *100
        num = cls.__decmillon(numeroInt)
        if (numero < 1000000): 
            return f"{num}DOLARES AMERICANOS {round(numeroDec,0)}/100 USD"
        else:
            return f"{num}DE DOLARES AMERICANOS {round(numeroDec,0)}/100 USD"




    
   
        
