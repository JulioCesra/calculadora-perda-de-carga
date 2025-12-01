import streamlit as st
from calculadora import calculadora_perda_de_carga
import os

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

if 'numero_reynolds' not in st.session_state:
    st.session_state['numero_reynolds'] = None
if 'regime_escoamento' not in st.session_state:
    st.session_state['regime_escoamento'] = None
if 'diametro_interno' not in st.session_state:
    st.session_state['diametro_interno'] = 0.15
if 'velocidade_escoamento' not in st.session_state:
    st.session_state['velocidade_escoamento'] = 2.5 
if 'fator_de_atrito' not in st.session_state:
    st.session_state['fator_de_atrito'] = None
if 'rugosidade_absoluta' not in st.session_state:
    st.session_state['rugosidade_absoluta'] = 4.5e-5


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
        Para calcular o coeficiente de atrito $$f$$ é preciso previamente calcular o **Número de Reynolds** ($$Re$$).
        
        **Fórmula para calcular o Número de Reynolds ($$Re$$):**
        '''
        )
    st.latex(
        body = r'''
        Re = \frac{v \times D}{ν} 
        '''
        )
    st.markdown(
        body = '''
        Onde:
        
        * $$v$$ é a velocidade média do fluido, em metros por segundo.
        * $$D$$ é o diâmetro, em metros:
            * Em **tubos e dutos:** Geralmente é o **diâmetro interno** ($$D$$).
            * Em **escoamento sobre placas:** É o **comprimento da placa.**
            * Em **escoamento em canais abertos:** Pode ser o **raio hidráulico** ($$Rh$$​).
        * $$ν$$ é a viscosidade cinemática, em metros quadrados por segundo.

        ---
        
        **CALCULAR NÚMERO DE REYNOLDS:**
        '''
        )

    velocidade_media_fluido = st.number_input(
        label = 'Digite a velocidade média do fluido, em metros por segundos (m/s):',
        format = '%.6f',
        min_value = 0.00
        )
    diametro_interno = st.number_input(
        label = 'Digite o diâmetro interno do tudo, em metros:',
        format = '%.6f',
        min_value = 0.00
        )
    viscosidade_cinematica = st.number_input(
        label = 'Digite a viscosidade cinemática, em metros quadrados por segundo (m²/s):',
        format = '%.6e',
        min_value = 0.00
        )
    esquerda, meio, direita = st.columns(3)
    realizar_calculo = meio.button(
        label = 'Calcular Número de Reynolds'
        )
    if realizar_calculo:
        try:
            numero_reynolds = equacoes.calculo_numero_reynolds(
                viscosidade_cinematica = viscosidade_cinematica,
                velocidade_media_fluido = velocidade_media_fluido,
                diametro_interno = diametro_interno
                )
            st.session_state['numero_reynolds'] = numero_reynolds
            st.session_state['diametro_interno'] = diametro_interno 
            st.session_state['velocidade_escoamento'] = velocidade_media_fluido
            st.session_state['fator_de_atrito'] = None
            st.markdown(
                body = '''
                ---
                
                **Resultado:**
                '''
                )
            st.latex(
                body = f'''
                Re = {numero_reynolds:.2f}
                '''
                )
            numero_reynolds_formatado = float(numero_reynolds.__format__('.2f'))
            if numero_reynolds_formatado < 2000:
                st.session_state['regime_escoamento'] = 'LAMINAR'
                st.markdown(
                    body = f'''
                    O resultado $$Re = {str(numero_reynolds_formatado)}$$ é menor que **2000**, o que indica que o escoamento do fluido é **laminar**.
                    '''
                    )
                st.markdown(
                    body = '**Representação:**'
                    )
                fluxo_laminar_representacao = os.path.join('..','img','fluxo_laminar.jpg')
                st.image(
                    image = fluxo_laminar_representacao
                    )
            elif numero_reynolds_formatado < 4000:
                st.session_state['regime_escoamento'] = 'TRANSICAO'
                st.markdown(
                    body = '''
                    O escoamento é **instável**.
                    '''
                    )
            elif numero_reynolds_formatado >= 4000:
                st.session_state['regime_escoamento'] = 'TURBULENTO'
                st.markdown(
                    body = f'''
                    O resultado $$Re = {str(numero_reynolds_formatado)}$$ é maior que **4000**, o que indica que o escoamento do fluido é **turbulento**.
                    '''
                    )
                st.markdown(
                    body = '**Representação:**'
                    )
                fluxo_turbulento_representacao = os.path.join('..','img','fluxo_turbulento.jpg')
                st.image(
                    image = fluxo_turbulento_representacao
                    )
        except ZeroDivisionError:
            st.error(
                body = 'A viscosidade cinemática não pode ser igual a zero!'
                )
        #st.rerun()

    if st.session_state['regime_escoamento'] == 'TURBULENTO':
        st.markdown(
            body = r'''
                    
                    ---
                
            A **Rugosidade Relativa** ($$\frac{ε}{D}$$) é um parâmetro adimensional essencial usado para calcular o fator de atrito ($$f$$) no regime de escoamento turbulento.
            
            Ela é calculada dividindo a **rugosidade absoluta** ($$ε$$) pelo **diâmetro interno** do tubo ($$D$$).
            '''
            )
        st.markdown(
            body = '''
            **Fórmula da Regosidade Relativa:**
            '''
            )
        st.latex(
            body = r'''
            Rugosidade Relativa = \frac{ε}{D}
            '''
            )
        st.markdown(
                    body = r'''
                    Onde:
                    * $ε$ **(epsilon)** é a rugosidade absoluta, em metros.
                    * $$D$$ é o diâmetro interno do tudo, em metros.
                    '''
                    )
        st.markdown(
                    body = r'''
                    **Determinando a rugosidade absoluta ($$ε$$)**
                    |Material da Tubulação Rugosidade|Rugosidade Absoluta Média ($$ε$$)|
                    |-------------------------------|----------------------|
                    |Tubos Lisos (Vidro, Plástico novo - PVC)|$$\approx 0.0015 \times 10^{-3} \ m$$|
                    |Cobre ou Latão|$$0.0015 \times 10^{-3} \ m$$
                    |Aço Comercial (Novo)|$$0.045 \times 10^{-3} \ m$$
                    |Ferro Fundido (Novo)|$$0.26 \times 10^{-3} \ m$$
                    |Concreto|$$0.3 \ \text{a} \ 3.0 \times 10^{-3} \ m$$

                    ---
                    
                    **CALCULAR RUGOSIDADE RELATIVA:**
                    '''
                    )
        rugosidade_absoluta = st.number_input(
                    label = 'Digite a rugosidade absoluta:',
                    format = '%.6e',
                    min_value = 0.00
                    )
        calcular_rugosidade_relativa = st.button(
                    label = 'Calcular Rugosidade Relativa'
                    )
        if calcular_rugosidade_relativa:
            try:
                rugosidade_relativa = equacoes.calculo_rugosidade_relativa(
                rugosidade_absoluta = rugosidade_absoluta,
                diametro_interno = st.session_state['diametro_interno'] 
                )
                st.markdown(
                body = '''
                ---
                ### Resultado da Rugosidade Relativa
                '''
                )
                st.markdown(
                body = r'''
                O valor da Rugosidade Relativa ($$\frac{ε​}{D}$$) é:
                '''
                )
                st.latex(
                    body = f'''
                    \\frac{{\\varepsilon}}{{D}} = {rugosidade_relativa:.4e}
                    '''
                )
        
                st.markdown(
                body = r'''
                    ---
            
                    Com o **Número de Reynolds** ($$Re$$) e a **Rugosidade Relativa** ($\frac{ε​}{D}$), o próximo passo é calcular o **Fator de Atrito ($$f$$)**, que será usado na Equação de Darcy-Weisbach.
            
                    A forma mais eficiente de calcular $$f$$ em código Python para escoamento turbulento é usando a **Fórmula Explícita de Swamee-Jain**, uma aproximação altamente precisa da Equação de Colebrook-White.
                    '''
                )
        
                st.markdown(
                body = r'''
                **Fórmula de Swamee-Jain (para $$f$$):**
                '''
                )
        
                st.latex(
                    r'''
                    f = \frac{0.25}{\left[\log_{10} \left( \frac{\varepsilon/D}{3.7} + \frac{5.74}{Re^{0.9}} \right) \right]^2}
                    '''
                )
        
                st.markdown(
                body = r'''
                **Onde:**
                * $$\frac{ε​}{D}$$ é a Rugosidade Relativa (calculada acima).
                * $$Re$$ é o Número de Reynolds.

                ---
                
                Aplicando os resultados anteriores da rugosidade relativa e do número de reynolds, o fator de atrito ($f$) calculado foi de:
                '''
                )
                fator_de_atrito = equacoes.calculo_coeficiente_de_atrito(
                    numero_reynolds = st.session_state['numero_reynolds'],
                    rugosidade_relativa = rugosidade_relativa
                    )
                st.latex(
                    body = f'''
                    f = {fator_de_atrito}
                    '''
                    )
                st.session_state['fator_de_atrito'] = fator_de_atrito
                                    
            except ZeroDivisionError:
                st.error(
                    body = 'O comprimento do diâmetro do tubo não pode igual a zero!'
                    )

    if st.session_state['fator_de_atrito'] is not None and st.session_state['fator_de_atrito'] != 0.0:
        f_final = st.session_state['fator_de_atrito']
        D_final = st.session_state['diametro_interno']
        V_final = st.session_state['velocidade_escoamento']
        st.markdown(
            body = '''
            ---
            **CALCULO DA FÓRMULA DE DARCY-WEISBACH:**
            '''
            )
        comprimento_da_tubulacao = st.number_input(
            label = 'Digite o comprimento da tubulação, em metros:',
            format = '%.6f',
            min_value = 0.00
        )
        realizar_calculo = st.button(
            label = 'Calcular Perda de Carga Distribuída'
        )
        if realizar_calculo:
            try:
                perda_de_carga_distribuida = equacoes.calculo_perda_de_carga_distribuida(
                    fator_de_atrito = f_final,
                    comprimento_da_tubulacao = comprimento_da_tubulacao,
                    diametro_interno_da_tubulacao = D_final,
                    velocidade_media_do_escoamento = V_final
                )
                st.markdown("---")
                st.markdown("## Resultado Final")
                st.markdown(f"O valor da **Perda de Carga Distribuída ($$h_f$$)** é:")
                st.latex(f"h_f \\approx {perda_de_carga_distribuida:.4f} \\text{{ m}}")
                st.success(
                    f'''
                    Isso significa que o fluido perde o equivalente a **{perda_de_carga_distribuida:.4f} metros de coluna de fluido** de energia
                    ao longo dos **{comprimento_da_tubulacao:.2f} metros** de tubulação.
                    '''
                )
            except ZeroDivisionError:
                    st.error('O Diâmetro Interno ($$D$$) não pode ser igual a zero para o cálculo de Darcy-Weisbach.')

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