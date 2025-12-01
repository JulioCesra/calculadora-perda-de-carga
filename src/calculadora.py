from typing import Union
import numpy as np
class calculadora_perda_de_carga():
    def __init__(self):
        self.ACELERACAO_GRAVITACIONAL = 9.81
        
    def perda_de_carga_localizada(
        self,
        coeficiente_especifico: Union[int, float],
        velocidade_media_escoamento: Union[int, float]
        ) -> Union[int, float]:

        validacao_tipos = (int, float)
        if not type(coeficiente_especifico) in validacao_tipos:
            raise TypeError(f"O coeficiente específico fornecido não é númerico. Você forneceu o valor: {coeficiente_especifico}.")
        if not type(velocidade_media_escoamento) in validacao_tipos:
            raise TypeError(f"A velocidade média de escoamento fornecida não é númerica. Você forneceu o valor: {velocidade_media_escoamento}.")        

        perda_carga_localizada = coeficiente_especifico * (pow(velocidade_media_escoamento,2) / (2 * self.ACELERACAO_GRAVITACIONAL))
        return perda_carga_localizada
    
    def calculo_numero_reynolds(
        self,
        viscosidade_cinematica: Union[int, float],
        velocidade_media_fluido: Union[int, float],
        diametro_interno: Union[int, float]
        ) -> Union[int, float]:

        if viscosidade_cinematica == 0.00:
            raise ZeroDivisionError(
                'Não é possível realizar o cálculo com a viscosidade cinemática igual a zero!'
                )
        
        numero_reynolds = (velocidade_media_fluido * diametro_interno) / viscosidade_cinematica
        return numero_reynolds

    def calculo_rugosidade_relativa(
        self,
        rugosidade_absoluta: Union[int, float],
        diametro_interno: Union[int, float]
        ) -> Union[int, float]:
        rugosidade_relativa = rugosidade_absoluta / diametro_interno
        return rugosidade_relativa
    
    def calculo_coeficiente_de_atrito(
        self,
        numero_reynolds: Union[int, float],
        rugosidade_relativa: Union[int, float]
        ) -> Union[int, float]: 
        if numero_reynolds <= 0:
            return 0
        
        if numero_reynolds < 2000:
            return 64 / numero_reynolds
        
        elif numero_reynolds >= 4000:
            try:
                termo_log = (rugosidade_relativa / 3.70) + (5.74 / pow(numero_reynolds, 0.9))
                denominador = pow(np.log10(termo_log), 2)
                fator_atrito = 0.25 / denominador
                return fator_atrito
            except Exception:
                return 0
        return 0

    def calculo_perda_de_carga_distribuida(
        self,
        fator_de_atrito: Union[int, float],
        comprimento_da_tubulacao: Union[int, float],
        diametro_interno_da_tubulacao: Union[int, float],
        velocidade_media_do_escoamento: Union[int, float]
        ) -> Union[int, float]:
        perda_carga_distribuida = fator_de_atrito * (comprimento_da_tubulacao / diametro_interno_da_tubulacao) * (pow(velocidade_media_do_escoamento,2) / (2 * self.ACELERACAO_GRAVITACIONAL))
        return perda_carga_distribuida