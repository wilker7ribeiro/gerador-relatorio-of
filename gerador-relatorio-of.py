import subprocess
import sys
import re
from datetime import datetime  
from operator import attrgetter
from collections import defaultdict



inputArgs = sys.argv
if len(inputArgs) < 4:
    print('usage python3 ../teste.py <project_cwd> <Author> <Periodo> <nome-projeto> <baseProjetoGit> <ultimo_commit_id> <task-filtro1> <task-filtro2>...')
    exit()


project_cwd = inputArgs[1]
author = inputArgs[2]
period = inputArgs[3]
nomeProjeto = inputArgs[4]
baseProjetoGit = inputArgs[5]
# resultado_tasks = {}
artefatos = []
renomeacoes = []
delecoes = []
ultimo_commit_id = inputArgs[6]
filter_tasks = inputArgs[7:]
from_file = False
base_url = 'https://fontes.intranet.bb.com.br' 

if from_file:
    with open('/kdi/git/gerador-relatorio-of/data_real.txt', 'r') as file:
        result =  file.read()
else: 
    stdout,stderr = subprocess.Popen(['git', 'log', period, '--name-status'] if period else ['git', 'log', '--name-status'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        cwd=project_cwd
    ).communicate()
    result = stdout.decode('utf-8')


commits_data = re.findall('commit (.*)\n?Author: (.*)\nDate:   (.*)\n\n((.*\n)+?)\n(((A|M|R|D).+\n)+)', result)

class Commit:
    def __init__(self, id, text, task, data, author, arquivos):
        self.id = id
        self.text = text
        self.task = task
        self.data = data
        self.author = author
        self.arquivos = arquivos

class Arquivo:
    def __init__(self, commit_id, operacao, nome, nome_antigo, nome_original = ''):
        self.commit_id = commit_id
        self.operacao = operacao
        self.nome = nome
        self.nome_original = nome_original if nome_original else nome
        self.nome_antigo = nome_antigo

class Renomeacao:
    def __init__(self, nome_novo, nome_antigo, data):
        self.nome_novo = nome_novo
        self.nome_antigo = nome_antigo
        self.data = data

class Task:
    def __init__(self, numero, commits, artefatos):
        self.numero = numero
        self.commits = commits
        self.artefatos = artefatos

    def get_ultimo_commit(self):
        return max(self.commits, key=attrgetter('data'))

class Artefato(Arquivo):
    def __init__(self, arquivo: Arquivo, commits: Commit, task):
        self.commits = commits
        self.task = task
        super().__init__(arquivo.commit_id, arquivo.operacao, arquivo.nome, arquivo.nome_antigo, arquivo.nome_original)

    def primeiro_commit_do_autor(self, author):
        for commit in reversed(self.commits):
            if (not len(filter_tasks) or commit.task in filter_tasks) and author in commit.author:
                return commit



class ItemPlanilha:
    def __init__(self, cells, exts, operacao, itens):
        self.cells = cells
        self.exts = exts
        self.operacao = operacao
        self.itens = itens

def make_arquivo(linha, commit_id):
    parts = linha.split('\t')
    operacao = parts[0]
    nome = parts[1] if len(parts) < 3 else parts[2]
    nome_antigo = None if len(parts) < 3 else parts[1]
    return Arquivo(commit_id, operacao, nome, nome_antigo)


def make_commit_from_string(commits_data):
    commit_id = commits_data[0]
    commit_author = commits_data[1]
    commit_date_string = commits_data[2]
    commit_text = commits_data[3].strip()
    task_finds = re.findall('((T|t)ask )(\d+)', commit_text)
    commit_task = commit_text if not task_finds else task_finds[0][2]
    arquivos = list(map(lambda linha: make_arquivo(linha, commit_id), filter(None, commits_data[5].split('\n'))))
    return Commit(commit_id, commit_text, commit_task, datetime.strptime(commit_date_string, '%a %b %d %H:%M:%S %Y %z'), commit_author, arquivos)




def print_planilha(com_commit = False):
    itens_planilha = [
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação JavaScript', ['.ts', '.js', '.tsx', '.vue'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração JavaScript', ['.ts', '.js', '.tsx', '.vue'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html', '.mako'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de tela HTML ou XHTML ou JSP ou XML ou VTL ou XSL ou Swing ou AWT ou XUI ou PHP', ['.html', '.mako'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração CSS ou SCSS', ['.css', '.scss', 'sass', 'less'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de objetos de Integração e Negócio Java', ['.java', '.scala', '.go'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de Objetos de Integração e Negócio Java', ['.java', '.scala', '.go'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Criação de arquivo chave/valor ou tipo xml', ['.json', '.xml', '.properties', 'requirements.txt'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Plataforma Distribuída 	Alteração de arquivo chave/valor ou tipo xml', ['.json', '.xml', '.properties', 'requirements.txt'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Criação de módulo em Python', ['.py'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de módulo em Python', ['.py'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Elaboração e criação de arquivo de definição "Dockerfile"', ['Dockerfile', 'Dockerfile-local', 'DockerfileLocal'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de arquivo de definição "Dockerfile"', ['Dockerfile', 'Dockerfile-local', 'DockerfileLocal'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Elaboração de documentação README e documentos auxiliares da aplicação', ['.md', '.MD'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Elaboração de documentação README e documentos auxiliares da aplicação', ['.md', '.MD'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Construção/Alteração de arquivos requirements ou values para deploy no ambiente Cloud', ['values.yaml', 'requirements.yaml', 'service.yaml', 'ingress.yaml'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Implementação de aplicação Cloud	Construção/Alteração de arquivos requirements ou values para deploy no ambiente Cloud', ['values.yaml', 'requirements.yaml', 'service.yaml', 'ingress.yaml'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Elaboração e criação de arquivo de definição "Docker Compose"', ['docker-compose.yaml', 'docker-compose.yml'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de arquivo de definição "Docker Compose"', ['docker-compose.yaml', 'docker-compose.yml'], 'M', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Criação de scripts Shell em JavaScript, Shell, PowerShell, PowerCli ou linguagem de construção de scripts equivalente, utilizado para automação de construção de infraestrutura de TI', ['.sh'], 'A', []),
        ItemPlanilha('IMPLEMENTAÇÃO DE SOFTWARE	Software de Infraestrutura 	Alteração de scripts Shell em JavaScript, Shell, PowerShell, PowerCli ou linguagem de construção de scripts equivalente, utilizado para automação de construção de infraestrutura de TI', ['.sh'], 'M', [])        
    ]


    for arquivo in artefatos: 
        # if arquivo.nome.endswith('__init__.py'):
        #     continue
        config = next(filter(lambda item_plan: item_plan.operacao == arquivo.operacao and any(arquivo.nome.endswith(ext) for ext in item_plan.exts), itens_planilha), None)
        if config:
            config.itens.append(arquivo)
        else:
            print('Configuração não encontrada para arquivo: ' + arquivo.operacao + ' ' + arquivo.nome)
    print('')

    for item_planilha in itens_planilha:
        soma = 0
        string = ''

        item_planilha.itens.sort(key=lambda r: r.task, reverse=True)
        string += '\n'
        grouped_by_task = defaultdict(list)
        for obj in item_planilha.itens:
            grouped_by_task[obj.task].append(obj)
        if com_commit:
            def make_task_part(task):
                def make_artefato_part(artefato: Artefato):
                    artefato_part = 'Task\t\t\t' + artefato.task + '\n'
                    artefato_part += 'Versao final:\t\t' + base_url + '/'+baseProjetoGit+ '/-/blob/' + ultimo_commit_id + '/' + artefato.nome + '\n'
                    artefato_part += 'Primeiro commit:\t' + base_url + '/'+baseProjetoGit+ '/-/blob/' + artefato.primeiro_commit_do_autor(author).id[:10] + '/' + artefato.nome_original + '\n'
                    return artefato_part
                return '\n'.join(list(map(make_artefato_part, grouped_by_task[task])))
            string += '\n\n'.join(map(lambda task: make_task_part(task), grouped_by_task.keys()))
        else:
            def make_task_part(task):
                task_str = 'Task '+task+'\n'
                task_str += '\n'.join(list(map(lambda i : (base_url + '/' + baseProjetoGit + '/-/blob/'+nomeProjeto+'/' + i.nome + '#' + ultimo_commit_id ), grouped_by_task[task])))
                return task_str
            string += '\n\n'.join(map(lambda task: make_task_part(task), grouped_by_task.keys()))
        string += '\n'
        soma += len(item_planilha.itens)
        if soma:

            print('======', item_planilha.cells, soma)
            print(string)


commits = list(map(make_commit_from_string, commits_data))
commits.sort(key=lambda r: r.data, reverse=True)


def get_nomeacao_final_rec(arquivo_nome, data, last_renomeacao):
    renomeacao = get_next_nomeacao(arquivo_nome, data)
    if not renomeacao:
        return last_renomeacao
    return get_nomeacao_final_rec(renomeacao.nome_novo, renomeacao.data, renomeacao)


def get_next_nomeacao(arquivo_nome, data):
    return next(filter(lambda r: r.data >= data and r.nome_antigo == arquivo_nome, renomeacoes), None)


for commit in commits:
    for arquivo in commit.arquivos:
        if not arquivo.operacao or not arquivo.nome:
            continue
        if arquivo.operacao.startswith('R'):
            renomeacao_nome_novo = arquivo.nome
            renomeacao_nome_antigo = arquivo.nome_antigo
            renomeacoes.append(Renomeacao(renomeacao_nome_novo, renomeacao_nome_antigo, commit.data))

            renomeacao_final = get_nomeacao_final_rec(arquivo.nome, commit.data, None)
            if renomeacao_final:
                arquivo.nome_original = arquivo.nome
                arquivo.nome = renomeacao_final.nome_novo

            if arquivo.operacao[1:] == '100':
                artefato = next(filter(lambda i: i.nome == arquivo.nome, artefatos), None)
                if artefato:
                    artefato.commits.append(commit)

                continue
            arquivo.operacao = 'M'
        else:
            renomeacao_final = get_nomeacao_final_rec(arquivo.nome, commit.data, None)
            if renomeacao_final:
                arquivo.nome_original = arquivo.nome
                arquivo.nome = renomeacao_final.nome_novo

        if arquivo.nome in delecoes:
            continue
        
        if arquivo.operacao == 'D':
            delecoes.append(arquivo.nome)
            continue

        if author not in commit.author:
            continue

        artefato = next(filter(lambda i: i.nome == arquivo.nome, artefatos), None)
        if artefato:
            if not len(filter_tasks) or commit.task in filter_tasks:
                if artefato.operacao != 'A' and arquivo.operacao == 'A':
                    artefato.operacao = arquivo.operacao
                artefato.task = commit.task
            artefato.commits.append(commit)
            continue
        if not len(filter_tasks) or commit.task in filter_tasks:
            artefatos.append(Artefato(arquivo, [commit], commit.task))



print('============================== RESULTADO============================= ')

print_planilha(com_commit=True)
print('')
print('')
print('')
print('')
print('============================== RESULTADO PARA PLANILHA ============================= ')
print('')
print_planilha()


#git log 649745097d8135f5b8eb6c1678ab9e2330401391...a30159ec30273f624a5efd4aa027e136e0ed8d54^1 --author=C1317576 --name-status
