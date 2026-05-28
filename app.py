import streamlit as st
from datetime import datetime
from banco_alunos import Banco

# --------------------------------------------- Configurações gerais

banco = Banco() # Instancia do gerenciador do banco de dados

st.set_page_config(layout='wide') # Configura layout do streamlit

# -------------------------------------------- SIDEBAR

st.sidebar.title('Sistema de Presença')

turma = st.sidebar.selectbox('Selecione a turma:', banco.turmas)

# -------------------------------------------- BODY
presenca, historico = st.tabs(['Registrar Presença', 'Histórico'])

with presenca:
    dia = datetime.today()
    st.title(turma)
    st.subheader(f'{dia.day}/0{dia.month}/2026')
    st.markdown('---')

    # Lista de nomes original da turma
    lista_original = banco.alunos[banco.alunos['turma'] == turma]['nome_aluno'].tolist()

    # Consulta no banco os alunos presentes no dia atual (lista de dicionários)
    alunos_presentes = banco.consulta_presentes_dia(turma, dia.isoformat())

    # Cria lista de nomes de alunos presentes no dia
    presentes = []
    for aluno in alunos_presentes:
        presentes.append(aluno['aluno'])
    
    # faz uma cópia da lista original e remove os alunos que já tem presença no dia atual no banco de dados
    lista_alunos = lista_original.copy()
    for aluno in lista_original:
        if aluno in presentes:
            lista_alunos.remove(aluno)

    # Verifica se ainda existem alunos
    if lista_alunos:

        aluno = st.selectbox('Alunos', lista_alunos) # Caixa de seleção com os alunos que ainda não receberam presença

        if st.button('Confirmar presença'):

            banco.inserir(aluno, turma) # Método que insere presença no banco de dados

            lista_alunos.remove(aluno) # remove da lista o aluno que já recebeu presença
            st.success(f'{aluno} confirmado!')

            st.rerun()

    else:
        st.success('Todos os alunos receberam presença!') # aparece se todos os alunos já receberam presença no dia

    st.markdown('---')

    st.subheader(f'Alunos presentes: {len(presentes)}')

    for i in presentes:
        st.write(i)

with historico:
    st.title('Histórico de presenças')
    data = st.date_input('Escolha o dia:')

    consulta = banco.consulta_turma_dia(turma,data)
    st.dataframe(consulta)
    
    st.markdown('---')
    st.subheader('Pesquisa por Aluno')

    aluno = st.selectbox('Aluno(a):',lista_original)

    consulta_aluno = banco.consulta_turma_aluno(turma, aluno)
    
    st.write(consulta_aluno)