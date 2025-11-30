import streamlit as st
from calculadora import calculadora_perda_de_carga

equacoes = calculadora_perda_de_carga()

st.title(
    body='Calculadora de Perda de Carga'
    )

st.markdown(
    """
    ## O que é Perda de Carga?
    É um fenômeno que ocorre em tubulações quando um fluido escoa. Ela se refere à perda de energia que o fluido sofre devido ao atrito com as paredes da tubulação e com as mudanças de direção do fluxo.
    ### Pode ser dividida em dois tipos:
    * **Distribuída:** ocorre ao longo de toda a extensão da tubulação retilínea e de diâmetro constante. É causada pelo atrito entre o fluido e as paredes da tubulação.
    * **Localizada:** ocorre em pontos específicos da tubulação, como em curvas, reduções ou expansões. É causada pela mudança de direção do fluxo.
    ---
    """
    )
opcoes_calculo = st.selectbox(
    label="Selecione qual o tipo de calculo de peso deseja realizar.",
    options=['Distribuída','Localizada']
    )

if opcoes_calculo == 'Distribuída':
    st.markdown(
        body = "**Fórmula Utilizada (Darcy-Weisbach):**"
        )
    
    st.latex(r'''
        h_f = f \times \frac{L}{D} \times \frac{V^2}{2 \times g}
             ''')
             
    st.markdown(
        body = '''
        Onde:
        * $$h_f$$ é a perda de carga distribuída, em metros 
        * $$f$$ é o Coeficiente de Atrito de Darcy (adimensional)
        * $$L$$ é o Comprimento da tubulação, em metros
        * $$D$$ é o Diâmetro Interno da tubulação, em metros
        * $$V$$ é a Velocidade média do escoamento, em metros por segundo
        * $$g$$ é a aceleração da gravidade, em metros por segundo ao quadrado

        ---

        O coeficiente de atrito $$f$$ é determinado pelo **Número de Reynolds** ($$Re$$) e pela rugosidade do tubo:
        '''
        )
    st.markdown("### Regime Laminar ($$Re < 2000$$)")
    st.markdown(
        body = 'Neste regime de fluxo suave, o coeficiente de atrito ($$f$$) é calculado pela seguinte equação:'
        )
 
    st.latex(
        r'''
        f = \frac{64}{Re}
        '''
        )
        
    st.markdown("### Regime Turbulento ($$Re > 4000$$)")
    st.markdown(
        body = '''
        Neste regime caótico (o mais comum na engenharia), $$f$$ é calculado com base na rugosidade relativa ($$\epsilon / D$$) e no Número de Reynolds ($$Re$$).
        
        A fórmula mais precisa é a de **Colebrook-White** (que é implícita e exige solução iterativa):
        '''
        )
  
    st.latex(
        r'''
        \frac{1}{\sqrt{f}} = -2 \times \log_{10} \left( \frac{\epsilon}{3.7 \times D} + \frac{2.51}{Re \times \sqrt{f}} \right)
        '''
        )
    st.markdown(
        body = r'''
        Onde:
        * $$\frac{\epsilon}{D}$$ é a rugosidade relativa (adimensional – tabelado)
        * $$Re$$ é o número de Reynolds (adimensional)
        
        Fórmula explícita de **Swamee–Jain**, para aproximação do resultado:
        '''
        )
    st.latex(
        r'''
        f \approx \frac{0.25}{\left[\log_{10} \times \left( \frac{\epsilon}{3.7 \times D} + \frac{5.74}{Re^{0.9}} \right) \right]^2}
        '''
        )
    


elif opcoes_calculo == 'Localizada':
    st.markdown(
        body = "**Fórmula Utilizada:**"
        )
    st.latex(r'''
        hₗ = K \times (\frac{V²}{2 \times g})
             ''')
    st.markdown(
        body = """
        Onde:
        * hₗ é a perda de carga localizada, em metros
        * K é um coeficiente específico do acessório (tabelado)
        * V é a velocidade de escoamento, em metros por segundo
        * G é a aceleração da gravidade, em metros por segundo ao quadrado
        """
        )
    coeficiente_especifico = st.number_input(
        label = 'Digite o coeficiente específico do acessório: ',
        min_value=0.00,
        format = '%.2f'
        )
    velocidade_media_escoamento = st.number_input(
        label = 'Digite a velocidade média do escoamento em m/s (metros por segundo): ',
        min_value = 0.00,
        format = '%.2f'
        )
    resultado_calculo = equacoes.perda_de_carga_localizada(
        coeficiente_especifico = coeficiente_especifico,
        velocidade_media_escoamento = velocidade_media_escoamento
        )
    esquerda, meio, direita = st.columns(3)
    realizar_calculo = meio.button(
        label = 'Realizar cálculo',
        
        )
    if realizar_calculo:
        st.markdown("## Resultado")
        st.markdown(
        f'''
        O valor final da **Perda de Carga Localizada ($$h_l$$)** é de:
        '''
        )
        st.latex(f"h_l \\approx {resultado_calculo:.2f} \\text{{ m}}")
        st.markdown(
            body = f'''
            Isso significa que o fluido perde o equivalente a **{resultado_calculo:.2f} metros de altura de coluna de água** de energia ao passar por um trecho específico.
            '''
            )