from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(
 SUPABASE_URL,
 SUPABASE_KEY
)

class Banco(object):    

    def __init__(self):
        # self.alunos = pd.read_csv('dados/alunos.csv')
        self.alunos = pd.DataFrame(supabase.table('Alunos').select('*').execute().data)
        self.tabela = "Presenca"
        self.turmas = self.alunos['turma'].unique().tolist()

    
    def inserir(self, aluno, turma):

        response = supabase.table(self.tabela).insert({
            'aluno': aluno,
            'turma': turma,
            'data' : datetime.today().isoformat(),
            'dia' : datetime.today().day,
            'mes' : datetime.today().month
            }).execute()
        print(response.data)

    def consulta_turma_dia(self, turma, data):
        
        response = supabase.table(self.tabela).select("*").eq('turma', turma).eq('data',data).execute()
        return pd.DataFrame(response.data)

    
    def consulta_presentes_dia(self, turma, data):
        
        response = supabase.table(self.tabela).select("*").eq('turma', turma).eq('data', data).execute()
        return response.data
    
    def consulta_turma_aluno(self, turma, aluno):
        
        response = supabase.table(self.tabela).select("*").eq('turma', turma).eq('aluno', aluno).execute().data
        if len(response) == 0:
            return None
        else:
            return pd.DataFrame(response).sort_values(['mes', 'dia'])

