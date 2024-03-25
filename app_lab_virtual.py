import streamlit as st
import numpy as np
import plotly.graph_objs as go
import vibration_toolbox as vtb

st.set_page_config(layout="wide")

st.markdown(""" <div style='text-align:center;'>
            <h1> Laboratório Virtual Vibrações Mecânicas </h1>
            </div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Vibrações livres não-amortecidas (1GDL)", 
                           "Vibrações livres amortecidas (1GDL)",
                           "Vibrações forçada amortecidas (1GDL)",
                            "Trabalho 1"])

with tab1:
    st.markdown(""" <div style='text-align:center;'>
            <h2> Modelo de sistema massa-mola livre com 1 GDL </h2>
            </div>""", unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,1,1])
    def vibracao_livre_nao_amortecida(m, k, x0, v0, t):
        w = np.sqrt(k/m)
        A1 = x0
        A2 = v0 / w
        x = A1*np.cos(w*t) + A2*np.sin(w*t)
        return x, w

    with st.form(key="data_input_namor"):
        col1, col2 = st.columns([1,2])
        #m = col1.slider("Massa do sistema (kg): ", 1, 1000, 5)
        #k = col1.slider("Rigidez do sistema (N/m): ", 1, 100000, 150)
        #x0 = col1.slider("Posição inicial do sistema (m): ", 1, 100, 1)
        #v0 = col1.slider("Velocidade inicial do sistema (m/s): ", 0, 100, 0)
        m = col1.number_input("Massa do sistema (kg):")
        k = col1.number_input("Rigidez do sistema (N/m):")
        x0 = col1.number_input("Posição inicial (m): ")
        v0 = col1. number_input("Velocidade inicial (m/s): ")

        submitted = col1.form_submit_button(label="Simular")
        if submitted:
            t_inicial = 0.0
            t_final = 20.0
            num_pontos = 1000
            t = np.linspace(t_inicial, t_final, num_pontos)

            x = vibracao_livre_nao_amortecida(m, k, x0, v0, t)[0]
            wn = vibracao_livre_nao_amortecida(m, k, x0, v0, t)[1]
            x_max = max(x)

            # Criando o gráfico usando Plotly
            trace = go.Scatter(x=t, y=x, mode='lines', name='Posição (m)')
            layout = go.Layout(title='Vibração Livre não-amortecida (1 GDL)',
                            xaxis=dict(title='Tempo (s)'),
                            yaxis=dict(title='Posição (m)'),
                            showlegend=True,
                            hovermode='closest')
            fig = go.Figure(data=[trace], layout=layout)
            col2.plotly_chart(fig)

            col1.write(f"Frequência natural: {wn:.4f} rad/s")
            col1.write(f"Amplitude máxima: {x_max:.4f} m")

with tab2:

    st.markdown(""" <div style='text-align:center;'>
            <h2> Modelo de sistema massa-mola-amortecedor livre com 1 GDL </h2>
            </div>""", unsafe_allow_html=True)

    def vibracao_livre_amortecida(m,k,zeta,x0,v0,t):
        wn = np.sqrt(k/m)
        
        if zeta >= 0 and zeta < 1:
            wd = (wn)*(np.sqrt(1-zeta**2))
            A1 = x0
            A2 = (v0 + zeta*wn*x0)/((np.sqrt(1-zeta**2))*wn)
            x = (np.exp(-zeta*wn*t))*(A1*np.cos(wd*t) + A2*np.sin(wd*t))
            kind = "sub-amortecido"
        elif zeta == 1:
            wd = (wn)*(np.sqrt(1-zeta**2))
            A1 = x0
            A2 = v0 + wn*x0
            x = (A1 + A2*t)*np.exp(-wn*t)
            kind = "criticamente amortecido"
        elif zeta > 1:
            wd = (wn)*(np.sqrt(zeta**2 - 1))
            A1 = (x0*wn*(zeta+(np.sqrt(zeta**2 - 1))) + v0)/(2*wn*(np.sqrt(zeta**2 - 1)))
            A2 = (x0*wn*(zeta-(np.sqrt(zeta**2 - 1))) - v0)/(2*wn*(np.sqrt(zeta**2 - 1)))
            x = A1*(np.exp((-zeta+np.sqrt(zeta**2 - 1))*wn*t)) + A2*(np.exp((-zeta - np.sqrt(zeta**2 - 1))*wn*t))
            kind = "superamortecido"
        return x, wn, wd, kind
        

    with st.form(key="data_input_amor"):
        col1,col2 = st.columns([1,2])
        m = col1.number_input("Massa do sistema (kg): ")
        k = col1.number_input("Rigidez do sistema (N/m): ")
        zeta = col1.number_input("Fator de amortecimento: ")
        x0 = col1.number_input("Posição inicial do sistema (m): ")
        v0 = col1.number_input("Velocidade inicial do sistema (m/s): ")

        submitted = col1.form_submit_button(label="Simular")
        if submitted:
            t_inicial = 0.0
            t_final = 20.0
            num_pontos = 1000
            t = np.linspace(t_inicial, t_final, num_pontos)

            x = vibracao_livre_amortecida(m,k,zeta,x0,v0,t)[0]
            wn = vibracao_livre_amortecida(m, k, zeta, x0, v0, t)[1]
            wd = vibracao_livre_amortecida(m, k, zeta, x0, v0, t)[2]
            tipo = vibracao_livre_amortecida(m, k, zeta, x0, v0, t)[3]
            
            trace = go.Scatter(x=t, y=x, mode='lines', name='Posição (m)')
            layout = go.Layout(title=f'Vibração Livre amortecida (1 GDL) {tipo}',
                            xaxis=dict(title='Tempo (s)'),
                            yaxis=dict(title='Posição (m)'),
                            showlegend=True,
                            hovermode='closest')
            fig = go.Figure(data=[trace], layout=layout)
            col2.plotly_chart(fig)

            col1.write(f"Frequência natural: {wn:.4f} rad/s")
            col1.write(f"Frequência natural amortecida: {wd:.4f} rad/s")

with tab3:
    st.markdown(""" <div style='text-align:center;'>
            <h2> Modelo de sistema massa-mola-amortecedor forçado com 1 GDL </h2>
            </div>""", unsafe_allow_html=True)
    with st.form(key="data_input_amor_forc-2"):
        col1, col2, col3 = st.columns([1,2,2])
        col1.markdown(""" <div style='text-align:center;'>
            <h3> Parâmetros do sistema </h3>
            </div>""", unsafe_allow_html=True)
        m = col1.number_input("Massa do sistema (kg): ")
        zeta = col1.number_input("Fator de amortecimento: ")
        k = col1.number_input("Rigidez do sistema (N/m): ")
        x0 = col1.number_input("Deslocamento inicial (m): ")
        v0 = col1.number_input("Velocidade inicial (m/s): ")
        F0 = col1.number_input("Amplitude da força externa: ")
        wdr = col1.number_input("Frequência da força externa:")

        c_crit = 2*np.sqrt(k*m)
        c = zeta*c_crit

        col2.markdown(""" <div style='text-align:center;'>
            <h3> Faixa de frequência </h3>
            </div>""", unsafe_allow_html=True)
        freq_inicial = col2.slider("Frequencia inicial: ", 0, 250, 0)
        freq_final = col2.slider("Frequencia final: ", 0, 250, 10)

        def frf(x,t):
            tempo_amostragem = t[1] - t[0]
            n = len(t)
            frequencias = np.fft.fftfreq(n, d=tempo_amostragem)
            fft = np.fft.fft(x)

            return frequencias, fft


        submitted = col1.form_submit_button(label = "Simular")
        if submitted:
            t, x, v = vtb.forced_response(m=m, c=c, k=k, x0= x0, v0=v0, wdr=wdr, F0=F0, max_time=20)
            freq, amp = frf(x,t)

            trace = go.Scatter(x=t, y=x, mode='lines')
            layout = go.Layout(title=f'Vibração Forçada amortecida (1 GDL)',
                                xaxis=dict(title='Tempo (s)'),
                                yaxis=dict(title='Posição (m)'))
            fig = go.Figure(data=[trace], layout=layout)
            col2.plotly_chart(fig)

            trace_amp = go.Scatter(x=freq, y=20*np.log10(np.abs(amp)), mode='lines')
            layout_amp = go.Layout(title=f'FRF Vibração forçada amortecida (1 GDL)',
                                   xaxis=dict(title='Frequência (Hz)', range=[freq_inicial, freq_final]),
                                   yaxis=dict(title="Amplitude"))
            fig_amp = go.Figure(data=[trace_amp], layout=layout_amp)
            col3.plotly_chart(fig_amp)

            trace_fase = go.Scatter(x=freq, y=np.angle(amp)*180/np.pi, mode='lines')
            layout_fase = go.Layout(xaxis=dict(title='Frequência (Hz)', range=[freq_inicial, freq_final]),
                                    yaxis=dict(title="Fase"))
            fig_fase = go.Figure(data=[trace_fase], layout = layout_fase)
            col3.plotly_chart(fig_fase)

            col1.write(f"Frequência natural: {np.sqrt(k/m):.2f}")
            col1.write(f"Frequência natural amortecida: {(np.sqrt(k/m))*np.sqrt(1-zeta**2):.2f}")

with tab4:
    st.markdown(""" <div style='text-align:center;'>
            <h2> Projeto 1 </h2>
            </div>""", unsafe_allow_html=True)
    
    col1,col2,col3 = st.columns([2,1,1])
    col2.markdown(""" <div style='text-align:center;'>
            <h4> Alunos </h4>
            </div>""", unsafe_allow_html=True)   
    col1.image("https://raw.githubusercontent.com/felixfabio/lab_virtual_vibracoes/main/projeto_1.png")
    col1.image("https://raw.githubusercontent.com/felixfabio/lab_virtual_vibracoes/main/bancada_exemplo_projeto_1.png")
    col1.image("https://raw.githubusercontent.com/felixfabio/lab_virtual_vibracoes/main/esquema_proj1_livre_n_amor.png")
    col2.write("Christiano Ramos: m = 4794,86 kg")
    col2.write("Deivisson Cassio: m = 2131,05 kg")
    col2.write("Diego Reis: m = 1198,71 kg")
    col2.write("Matheus Machado: m = 767,18 kg")
    col2.write("Matheus Borges: m = 532,76 kg")
    col2.write("Matteus Bernardes: m = 391,41 kg")
    col2.write("Vinicius Reis: m = 299,68 kg")
    col2.markdown(""" <div style='text-align:center;'>
            <h4> Dados do projeto </h4>
            </div>""", unsafe_allow_html=True)
    col2.write("L = 61,5 mm")
    col2.write("h = 0,8 mm")
    col2.write("b = 22,45 mm")
    col2.write("E = 2 x 10E11 N/m²")
    col2.write("c = 4,036 N/m/s")
    col3.latex(r'''
                I_{xx} = \frac{bh^3}{12}
                ''')
    col3.latex(r'''
                k_{xx} = \frac{3EI_{xx}}{L^3}
                ''')
    col3.latex(r'''
                \eta = \{c}{2\sqrt{km}}
                ''')

    
    
    
    






    

