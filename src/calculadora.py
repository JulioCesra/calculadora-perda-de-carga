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
        Viscosidade_cinematica: Union[int, float],
        Velocidade_media_escoamento: Union[int, float],
        Diametro_interno_do_tubo: Union[int, float]
        ) -> Union[int, float]:
        numero_reynolds = (Velocidade_media_escoamento * Diametro_interno_do_tubo) / Viscosidade_cinematica
        return numero_reynolds, Diametro_interno_do_tubo

    def calculo_coeficiente_de_atrito(
        self,
        Numero_reynolds: Union[int, float],
        Diametro_interno_do_tubo: Union[int, float],
        Rugosidade_absoluta: Union[int, float]
        ) -> Union[int, float]: 
        if Numero_reynolds <= 0:
            return 0
        
        if Numero_reynolds < 2000:
            return 64 / Numero_reynolds
        
        elif Numero_reynolds >= 2000:
            rugosidade_relativa = Rugosidade_absoluta/ Diametro_interno_do_tubo
            try:
                termo_log = (rugosidade_relativa / 3.70) + (5.74 / pow(Numero_reynolds, 0.9))
                denominador = pow(np.log10(termo_log), 2)
                fator_atrito = 0.25 / denominador
                return fator_atrito
            except Exception:
                return 0
        return 0