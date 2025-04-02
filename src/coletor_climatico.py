"""
Sistema de Coleta de Dados Climáticos

Este script coleta dados climáticos de APIs meteorológicas (OpenWeather como primária e INMET como backup)
para regiões agrícolas predefinidas. O sistema coleta tanto dados históricos quanto atuais,
armazenando-os em formato CSV para uso em modelos preditivos.

Funcionalidades:
- Coleta de dados históricos (últimos 15 anos) 
- Coleta de dados recentes (últimos 7 dias)
- Fallback automático entre APIs
- Logs detalhados
- Prevenção de duplicação de dados
- Execução programável via cron
"""

import os
import sys
import json
import time
import logging
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Configuração de Logging
DIRETORIO_BASE = Path(__file__).parent.parent
DIRETORIO_LOGS = DIRETORIO_BASE / "logs"

# Organizar logs por ano/mês, semelhante aos dados
hoje = datetime.now()
diretorio_log_ano = DIRETORIO_LOGS / str(hoje.year)
diretorio_log_mes = diretorio_log_ano / f"{hoje.month:02d}"

# Criar diretórios de log se não existirem
diretorio_log_ano.mkdir(exist_ok=True, parents=True)
diretorio_log_mes.mkdir(exist_ok=True, parents=True)

arquivo_log = diretorio_log_mes / f"coletor_{hoje.strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(arquivo_log),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configurações do Sistema
CHAVE_API_OPENWEATHER = "0476cdfcc3da9e85452287b12c174cf1"  # Substitua pela sua API key real
TOKEN_INMET = "seu_token_aqui"  # Substitua pelo seu token real

# Diretórios de dados
DIRETORIO_BASE = Path(__file__).parent.parent
DIRETORIO_DADOS = DIRETORIO_BASE / "dados"
DIRETORIO_OPENWEATHER = DIRETORIO_DADOS / "openweather"
DIRETORIO_INMET = DIRETORIO_DADOS / "inmet"
DIRETORIO_CONFIG = DIRETORIO_BASE / "config"
DIRETORIO_LOGS = DIRETORIO_BASE / "logs"

# Garantir que os diretórios existam
DIRETORIO_OPENWEATHER.mkdir(exist_ok=True, parents=True)
DIRETORIO_INMET.mkdir(exist_ok=True, parents=True)
DIRETORIO_LOGS.mkdir(exist_ok=True, parents=True)

# Carregar credenciais das APIs
try:
    with open(DIRETORIO_CONFIG / "credenciais.json", "r", encoding="utf-8") as arquivo_credenciais:
        import json
        credenciais = json.load(arquivo_credenciais)
        CHAVE_API_OPENWEATHER = credenciais.get("openweather", {}).get("api_key", CHAVE_API_OPENWEATHER)
        TOKEN_INMET = credenciais.get("inmet", {}).get("token", TOKEN_INMET)
        logger.info("Credenciais das APIs carregadas com sucesso")
except Exception as e:
    logger.warning(f"Erro ao carregar arquivo de credenciais: {e}")
    logger.warning("Usando valores padrão para credenciais")

# Carregar regiões agrícolas do arquivo de configuração
try:
    with open(DIRETORIO_CONFIG / "regioes.json", "r", encoding="utf-8") as arquivo_regioes:
        import json
        config_regioes = json.load(arquivo_regioes)
        REGIOES_AGRICOLAS = config_regioes.get("regioes_agricolas", [])
        logger.info(f"Carregadas {len(REGIOES_AGRICOLAS)} regiões do arquivo de configuração")
except Exception as e:
    logger.error(f"Erro ao carregar arquivo de regiões: {e}")
    # Configuração padrão caso o arquivo não exista ou tenha erro
    logger.warning("Usando configuração padrão de regiões")
    REGIOES_AGRICOLAS = [
        {
            "nome": "Ribeirao_Preto_SP",
            "descricao": "Região de Ribeirão Preto - SP (Cana-de-açúcar)",
            "latitude": -21.17,
            "longitude": -47.81,
            "estacao_inmet": "A711" 
        },
        {
            "nome": "Brasilia_DF",
            "descricao": "Região de Brasília - DF (Soja e Milho)",
            "latitude": -15.78,
            "longitude": -47.93,
            "estacao_inmet": "A001"
        }
    ]

# Constantes de Configuração
MAX_TENTATIVAS = 3
ATRASO_TENTATIVA = 5  # segundos
ANOS_HISTORICO = 15


class ColetorDadosClimaticos:
    """
    Classe principal para coleta de dados climáticos das diferentes APIs.
    """
    
    def __init__(self):
        """Inicializa o coletor de dados climáticos."""
        logger.info("Inicializando o sistema de coleta de dados climáticos")
        # Verificar credenciais
        if CHAVE_API_OPENWEATHER == "sua_api_key_aqui":
            logger.warning("ATENÇÃO: API Key do OpenWeather não configurada")
        if TOKEN_INMET == "seu_token_aqui":
            logger.warning("ATENÇÃO: Token do INMET não configurado")
    
    def coletar_para_todas_regioes(self, modo="atual"):
        """
        Coleta dados para todas as regiões configuradas.
        
        Args:
            modo (str): "atual" para dados dos últimos 7 dias, "historico" para dados históricos
        """
        logger.info(f"Iniciando coleta no modo: {modo}")
        
        for regiao in REGIOES_AGRICOLAS:
            logger.info(f"Processando região: {regiao['nome']}")
            
            sucesso = False
            
            # Tentativa com OpenWeather (API Principal)
            try:
                logger.info(f"Tentando coleta com OpenWeather para {regiao['nome']}")
                if modo == "atual":
                    dados = self.coletar_openweather_atual(regiao)
                else:
                    dados = self.coletar_openweather_historico(regiao)
                    
                if dados is not None and not dados.empty:
                    self.salvar_dados(dados, regiao['nome'], "openweather", modo)
                    sucesso = True
                    logger.info(f"Coleta com OpenWeather bem-sucedida para {regiao['nome']}")
                else:
                    logger.warning(f"OpenWeather retornou dados vazios para {regiao['nome']}")
            
            except Exception as e:
                logger.error(f"Erro na coleta com OpenWeather para {regiao['nome']}: {str(e)}")
            
            # Se falhou com OpenWeather, tenta com INMET (API Backup)
            if not sucesso:
                logger.info(f"Ativando sistema de fallback para {regiao['nome']}")
                try:
                    logger.info(f"Tentando coleta com INMET para {regiao['nome']}")
                    if modo == "atual":
                        dados = self.coletar_inmet_atual(regiao)
                    else:
                        dados = self.coletar_inmet_historico(regiao)
                        
                    if dados is not None and not dados.empty:
                        self.salvar_dados(dados, regiao['nome'], "inmet", modo)
                        sucesso = True
                        logger.info(f"Coleta com INMET bem-sucedida para {regiao['nome']}")
                    else:
                        logger.warning(f"INMET retornou dados vazios para {regiao['nome']}")
                
                except Exception as e:
                    logger.error(f"Erro na coleta com INMET para {regiao['nome']}: {str(e)}")
            
            if not sucesso:
                logger.error(f"FALHA COMPLETA: Não foi possível obter dados para {regiao['nome']} usando nenhuma API")
    
    def coletar_openweather_atual(self, regiao):
        """
        Coleta dados climáticos atuais da API OpenWeather.
        
        Args:
            regiao (dict): Dicionário com informações da região
            
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados ou None em caso de falha
        """
        latitude = regiao['latitude']
        longitude = regiao['longitude']
        
        # URL para dados atuais
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={CHAVE_API_OPENWEATHER}&units=metric&lang=pt_br"
        
        # Fazer a requisição com retry em caso de falha
        for tentativa in range(MAX_TENTATIVAS):
            try:
                logger.debug(f"Tentativa {tentativa+1} para OpenWeather atual: {url}")
                resposta = requests.get(url, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()
                
                # Transformar os dados em DataFrame
                agora = datetime.now()
                dados_climaticos = {
                    'data': agora.strftime("%Y-%m-%d"),
                    'hora': agora.strftime("%H:%M:%S"),
                    'temperatura': dados['main']['temp'],
                    'sensacao_termica': dados['main']['feels_like'],
                    'temp_min': dados['main']['temp_min'],
                    'temp_max': dados['main']['temp_max'],
                    'pressao': dados['main']['pressure'],
                    'umidade': dados['main']['humidity'],
                    'velocidade_vento': dados['wind']['speed'] if 'wind' in dados else None,
                    'direcao_vento': dados['wind']['deg'] if 'wind' in dados else None,
                    'nuvens': dados['clouds']['all'] if 'clouds' in dados else None,
                    'clima_principal': dados['weather'][0]['main'] if 'weather' in dados and len(dados['weather']) > 0 else None,
                    'clima_descricao': dados['weather'][0]['description'] if 'weather' in dados and len(dados['weather']) > 0 else None,
                    'chuva_1h': dados['rain']['1h'] if 'rain' in dados and '1h' in dados['rain'] else 0,
                    'fonte': 'openweather',
                    'regiao': regiao['nome'],
                    'latitude': latitude,
                    'longitude': longitude
                }
                
                return pd.DataFrame([dados_climaticos])
                
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, 
                   requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                logger.warning(f"Erro ao acessar OpenWeather (tentativa {tentativa+1}): {e}")
                if tentativa < MAX_TENTATIVAS - 1:
                    time.sleep(ATRASO_TENTATIVA)
                else:
                    logger.error(f"Falha após {MAX_TENTATIVAS} tentativas com OpenWeather")
                    return None
            except Exception as e:
                logger.error(f"Erro inesperado ao processar dados OpenWeather: {e}")
                return None
    
    def coletar_openweather_historico(self, regiao):
        """
        Coleta dados históricos da API OpenWeather usando a API Historical Bulk.
        
        Args:
            regiao (dict): Dicionário com informações da região
            
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados ou None em caso de falha
        """
        latitude = regiao['latitude']
        longitude = regiao['longitude']
        
        # Lista para armazenar todos os dados coletados
        todos_dados = []
        
        # Calcular datas para coleta (últimos 15 anos)
        data_fim = datetime.now()
        data_inicio = data_fim.replace(year=data_fim.year - ANOS_HISTORICO)
        
        # Dividir em chunks anuais para evitar requisições muito grandes
        # e problemas de limite de API
        data_atual = data_inicio
        
        logger.info(f"Iniciando coleta de {ANOS_HISTORICO} anos de dados históricos para {regiao['nome']}")
        logger.info(f"Período: {data_inicio.strftime('%Y-%m-%d')} até {data_fim.strftime('%Y-%m-%d')}")
        
        while data_atual < data_fim:
            # Calcular próximo período (1 ano ou até data fim, o que for menor)
            proximo_periodo = min(
                data_atual.replace(year=data_atual.year + 1),
                data_fim
            )
            
            # Converter para timestamp Unix (segundos desde 1970-01-01)
            timestamp_inicio = int(data_atual.timestamp())
            timestamp_fim = int(proximo_periodo.timestamp())
            
            # URL para a API de dados históricos
            # Usando a API 3.0 que permite acesso a dados históricos
            url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={latitude}&lon={longitude}&dt={timestamp_fim}&appid={CHAVE_API_OPENWEATHER}&units=metric&lang=pt_br"
            
            logger.info(f"Coletando dados para {regiao['nome']} - período: {data_atual.strftime('%Y-%m-%d')} a {proximo_periodo.strftime('%Y-%m-%d')}")
            
            # Fazer a requisição com retry em caso de falha
            for tentativa in range(MAX_TENTATIVAS):
                try:
                    logger.debug(f"Tentativa {tentativa+1} para OpenWeather histórico: {url}")
                    resposta = requests.get(url, timeout=30)  # Timeout maior para dados históricos
                    resposta.raise_for_status()
                    dados = resposta.json()
                    
                    # Verificar se recebemos dados
                    if 'data' in dados and len(dados['data']) > 0:
                        # Processar cada ponto de dados
                        for ponto in dados['data']:
                            # Converter timestamp em data e hora
                            dt = datetime.fromtimestamp(ponto.get('dt', 0))
                            
                            # Criar dicionário de dados
                            dados_climaticos = {
                                'data': dt.strftime("%Y-%m-%d"),
                                'hora': dt.strftime("%H:%M:%S"),
                                'temperatura': ponto.get('temp', None),
                                'sensacao_termica': ponto.get('feels_like', None),
                                'pressao': ponto.get('pressure', None),
                                'umidade': ponto.get('humidity', None),
                                'ponto_orvalho': ponto.get('dew_point', None),
                                'indice_uv': ponto.get('uvi', None),
                                'nuvens': ponto.get('clouds', None),
                                'visibilidade': ponto.get('visibility', None),
                                'velocidade_vento': ponto.get('wind_speed', None),
                                'direcao_vento': ponto.get('wind_deg', None),
                                'rajada_vento': ponto.get('wind_gust', None),
                                'fonte': 'openweather',
                                'regiao': regiao['nome'],
                                'latitude': latitude,
                                'longitude': longitude,
                                'timestamp': ponto.get('dt', 0)
                            }
                            
                            # Adicionar informações de clima se disponíveis
                            if 'weather' in ponto and len(ponto['weather']) > 0:
                                dados_climaticos['clima_id'] = ponto['weather'][0].get('id', None)
                                dados_climaticos['clima_principal'] = ponto['weather'][0].get('main', None)
                                dados_climaticos['clima_descricao'] = ponto['weather'][0].get('description', None)
                                dados_climaticos['clima_icone'] = ponto['weather'][0].get('icon', None)
                            
                            # Adicionar informações de chuva e neve se disponíveis
                            if 'rain' in ponto:
                                dados_climaticos['chuva_1h'] = ponto['rain'].get('1h', 0)
                            if 'snow' in ponto:
                                dados_climaticos['neve_1h'] = ponto['snow'].get('1h', 0)
                            
                            # Adicionar ao conjunto de dados
                            todos_dados.append(dados_climaticos)
                        
                        logger.info(f"Coletados {len(dados['data'])} pontos de dados para {regiao['nome']} - {data_atual.strftime('%Y-%m-%d')}")
                        break  # Sair do loop de tentativas se bem-sucedido
                    else:
                        logger.warning(f"Sem dados para o período {data_atual.strftime('%Y-%m-%d')} a {proximo_periodo.strftime('%Y-%m-%d')}")
                        
                except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, 
                       requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                    logger.warning(f"Erro ao acessar OpenWeather histórico (tentativa {tentativa+1}): {e}")
                    if tentativa < MAX_TENTATIVAS - 1:
                        # Espera exponencial entre tentativas (5s, 10s, 20s...)
                        tempo_espera = ATRASO_TENTATIVA * (2 ** tentativa)
                        logger.info(f"Aguardando {tempo_espera}s antes da próxima tentativa...")
                        time.sleep(tempo_espera)
                    else:
                        logger.error(f"Falha após {MAX_TENTATIVAS} tentativas com OpenWeather para período {data_atual.strftime('%Y-%m-%d')}")
                except Exception as e:
                    logger.error(f"Erro inesperado ao processar dados históricos OpenWeather: {e}")
                    break
            
            # Avançar para o próximo período
            data_atual = proximo_periodo
            
            # Aguardar entre períodos para evitar limitação de API
            time.sleep(1)
        
        # Verificar se coletamos algum dado
        if not todos_dados:
            logger.warning(f"Nenhum dado histórico coletado para {regiao['nome']}")
            return pd.DataFrame()
        
        # Criar DataFrame com todos os dados coletados
        logger.info(f"Total de {len(todos_dados)} pontos de dados históricos coletados para {regiao['nome']}")
        return pd.DataFrame(todos_dados)
    
    def coletar_inmet_atual(self, regiao):
        """
        Coleta dados climáticos atuais do INMET para uma estação específica.
        
        Args:
            regiao (dict): Dicionário com informações da região, incluindo código da estação INMET
            
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados ou None em caso de falha
        """
        codigo_estacao = regiao['estacao_inmet']
        
        # Usando try/import para não quebrar se a biblioteca não estiver instalada
        try:
            from inmetpy import INMET
            inmet = INMET()  # Se tiver token: inmet = INMET(token=TOKEN_INMET)
            
            for tentativa in range(MAX_TENTATIVAS):
                try:
                    logger.debug(f"Tentativa {tentativa+1} para INMET atual: estação {codigo_estacao}")
                    
                    # Obter dados horários
                    dados_horarios = inmet.hourly_data(station_code=codigo_estacao)
                    
                    if dados_horarios is not None and not dados_horarios.empty:
                        # Filtrar apenas os dados dos últimos 7 dias
                        sete_dias_atras = datetime.now() - timedelta(days=7)
                        if 'DATETIME' in dados_horarios.columns:
                            dados_horarios['DATETIME'] = pd.to_datetime(dados_horarios['DATETIME'])
                            dados_recentes = dados_horarios[dados_horarios['DATETIME'] >= sete_dias_atras]
                        else:
                            dados_recentes = dados_horarios  # Se não tiver coluna de data, usa todos os dados
                        
                        # Adicionar metadados da região
                        dados_recentes['fonte'] = 'inmet'
                        dados_recentes['regiao'] = regiao['nome']
                        dados_recentes['latitude'] = regiao['latitude']
                        dados_recentes['longitude'] = regiao['longitude']
                        
                        return dados_recentes
                    
                    logger.warning(f"INMET retornou dados vazios para estação {codigo_estacao}")
                    if tentativa < MAX_TENTATIVAS - 1:
                        time.sleep(ATRASO_TENTATIVA)
                    else:
                        return None
                        
                except Exception as e:
                    logger.warning(f"Erro na tentativa {tentativa+1} para INMET: {e}")
                    if tentativa < MAX_TENTATIVAS - 1:
                        time.sleep(ATRASO_TENTATIVA * (tentativa + 1))  # Backoff exponencial
                    else:
                        logger.error(f"Falha após {MAX_TENTATIVAS} tentativas com INMET")
                        return None
        
        except ImportError:
            logger.error("Biblioteca inmetpy não instalada. Não é possível acessar dados do INMET.")
            return None
    
    def coletar_inmet_historico(self, regiao):
        """
        Coleta dados históricos do INMET.
        
        Args:
            regiao (dict): Dicionário com informações da região
            
        Returns:
            pandas.DataFrame: DataFrame com os dados históricos ou None em caso de falha
        """
        codigo_estacao = regiao['estacao_inmet']
        
        try:
            from inmetpy import INMET
            inmet = INMET()  # Se tiver token: inmet = INMET(token=TOKEN_INMET)
            
            # Lista para armazenar todos os dados coletados
            todos_dados = []
            
            # Calcular datas para coleta (últimos 15 anos)
            data_fim = datetime.now()
            data_inicio = data_fim.replace(year=data_fim.year - ANOS_HISTORICO)
            
            logger.info(f"Iniciando coleta de {ANOS_HISTORICO} anos de dados históricos do INMET para {regiao['nome']}")
            logger.info(f"Período: {data_inicio.strftime('%Y-%m-%d')} até {data_fim.strftime('%Y-%m-%d')}")
            
            try:
                # Verificar se a biblioteca inmetpy suporta coleta de dados históricos
                # A implementação depende dos recursos disponíveis na biblioteca
                if hasattr(inmet, 'daily_data'):
                    # Alguns casos a API do INMET limita a quantidade de dados por requisição
                    # Vamos dividir em chunks anuais
                    data_atual = data_inicio
                    
                    while data_atual < data_fim:
                        # Calcular próximo período (1 ano ou até data fim, o que for menor)
                        proximo_periodo = min(
                            data_atual.replace(year=data_atual.year + 1),
                            data_fim
                        )
                        
                        data_inicio_str = data_atual.strftime("%Y-%m-%d")
                        data_fim_str = proximo_periodo.strftime("%Y-%m-%d")
                        
                        logger.info(f"Coletando dados diários INMET para {regiao['nome']} - período: {data_inicio_str} a {data_fim_str}")
                        
                        # Tentar obter dados diários
                        try:
                            dados_diarios = inmet.daily_data(
                                station_code=codigo_estacao,
                                start_date=data_inicio_str,
                                end_date=data_fim_str
                            )
                            
                            if dados_diarios is not None and not dados_diarios.empty:
                                # Adicionar metadados da região
                                dados_diarios['fonte'] = 'inmet'
                                dados_diarios['regiao'] = regiao['nome']
                                dados_diarios['latitude'] = regiao['latitude']
                                dados_diarios['longitude'] = regiao['longitude']
                                
                                # Adicionar ao conjunto total
                                todos_dados.append(dados_diarios)
                                logger.info(f"Coletados {len(dados_diarios)} registros diários INMET para {regiao['nome']} - período {data_inicio_str} a {data_fim_str}")
                            else:
                                logger.warning(f"Sem dados diários INMET para {regiao['nome']} no período {data_inicio_str} a {data_fim_str}")
                        
                        except Exception as e:
                            logger.error(f"Erro ao coletar dados diários INMET para {regiao['nome']} - período {data_inicio_str} a {data_fim_str}: {e}")
                        
                        # Avançar para o próximo período
                        data_atual = proximo_periodo
                        
                        # Aguardar entre requisições para evitar sobrecarga
                        time.sleep(1)
                
                elif hasattr(inmet, 'historical_data'):
                    # Alternativa se a biblioteca tiver outro método para dados históricos
                    logger.info(f"Tentando método historical_data para {regiao['nome']}")
                    
                    data_inicio_str = data_inicio.strftime("%Y-%m-%d")
                    data_fim_str = data_fim.strftime("%Y-%m-%d")
                    
                    dados_historicos = inmet.historical_data(
                        station_code=codigo_estacao,
                        start_date=data_inicio_str,
                        end_date=data_fim_str
                    )
                    
                    if dados_historicos is not None and not dados_historicos.empty:
                        # Adicionar metadados da região
                        dados_historicos['fonte'] = 'inmet'
                        dados_historicos['regiao'] = regiao['nome']
                        dados_historicos['latitude'] = regiao['latitude']
                        dados_historicos['longitude'] = regiao['longitude']
                        
                        todos_dados.append(dados_historicos)
                        logger.info(f"Coletados {len(dados_historicos)} registros históricos INMET para {regiao['nome']}")
                    else:
                        logger.warning(f"Sem dados históricos INMET para {regiao['nome']}")
                
                else:
                    # Se não houver método específico para dados históricos
                    logger.warning(f"A biblioteca inmetpy não tem métodos para dados históricos. Tentando alternativa.")
                    
                    # Podemos tentar usar o método de dados horários com datas específicas se disponível
                    if hasattr(inmet, 'hourly_data_for_date'):
                        # Coletar dados mês a mês para os últimos anos
                        # Limitando a quantidade para não sobrecarregar
                        anos_coleta = min(5, ANOS_HISTORICO)  # Coletamos no máximo 5 anos de dados horários
                        
                        data_atual = data_fim.replace(year=data_fim.year - anos_coleta)
                        
                        while data_atual < data_fim:
                            # Avança mês a mês
                            mes_atual = data_atual.month
                            ano_atual = data_atual.year
                            
                            data_mes_str = f"{ano_atual}-{mes_atual:02d}-01"
                            logger.info(f"Coletando dados horários INMET para {regiao['nome']} - mês: {data_mes_str}")
                            
                            try:
                                dados_horarios = inmet.hourly_data_for_date(
                                    station_code=codigo_estacao,
                                    date=data_mes_str
                                )
                                
                                if dados_horarios is not None and not dados_horarios.empty:
                                    # Adicionar metadados da região
                                    dados_horarios['fonte'] = 'inmet'
                                    dados_horarios['regiao'] = regiao['nome']
                                    dados_horarios['latitude'] = regiao['latitude']
                                    dados_horarios['longitude'] = regiao['longitude']
                                    
                                    todos_dados.append(dados_horarios)
                                    logger.info(f"Coletados {len(dados_horarios)} registros horários INMET para {regiao['nome']} - mês {data_mes_str}")
                                else:
                                    logger.warning(f"Sem dados horários INMET para {regiao['nome']} no mês {data_mes_str}")
                            
                            except Exception as e:
                                logger.error(f"Erro ao coletar dados horários INMET para {regiao['nome']} - mês {data_mes_str}: {e}")
                            
                            # Avançar para o próximo mês
                            if mes_atual == 12:
                                data_atual = data_atual.replace(year=ano_atual + 1, month=1)
                            else:
                                data_atual = data_atual.replace(month=mes_atual + 1)
                            
                            # Aguardar entre requisições
                            time.sleep(1)
                    else:
                        logger.error(f"Não foi possível encontrar método adequado na biblioteca inmetpy para dados históricos")
            
            except Exception as e:
                logger.error(f"Erro geral ao coletar dados históricos INMET: {e}")
            
            # Verificar se coletamos algum dado
            if not todos_dados:
                logger.warning(f"Nenhum dado histórico do INMET coletado para {regiao['nome']}")
                return pd.DataFrame()
            
            # Combinar todos os DataFrames coletados
            dados_combinados = pd.concat(todos_dados, ignore_index=True)
            
            # Remover possíveis duplicatas (por data/hora)
            if 'DATETIME' in dados_combinados.columns:
                dados_combinados = dados_combinados.drop_duplicates(subset=['DATETIME'])
            
            logger.info(f"Total de {len(dados_combinados)} registros históricos do INMET coletados para {regiao['nome']}")
            return dados_combinados
            
        except ImportError:
            logger.error("Biblioteca inmetpy não instalada. Não é possível acessar dados do INMET.")
            return None
    
    def salvar_dados(self, dados, nome_regiao, fonte, modo):
        """
        Salva os dados coletados em formato CSV.
        
        Args:
            dados (pandas.DataFrame): DataFrame com os dados a serem salvos
            nome_regiao (str): Nome da região
            fonte (str): Fonte dos dados (openweather ou inmet)
            modo (str): Modo de coleta (atual ou historico)
        """
        if dados is None or dados.empty:
            logger.warning(f"Não há dados para salvar: {nome_regiao}, {fonte}, {modo}")
            return
        
        # Definir diretório de destino
        diretorio_destino = DIRETORIO_OPENWEATHER if fonte == "openweather" else DIRETORIO_INMET
        
        # Criar subdiretórios por ano e mês
        hoje = datetime.now()
        diretorio_ano = diretorio_destino / str(hoje.year)
        diretorio_mes = diretorio_ano / f"{hoje.month:02d}"
        
        diretorio_ano.mkdir(exist_ok=True)
        diretorio_mes.mkdir(exist_ok=True)
        
        # Nome do arquivo baseado no modo, região e data
        data_str = hoje.strftime("%Y%m%d")
        caminho_arquivo = diretorio_mes / f"{modo}_{nome_regiao}_{data_str}.csv"
        
        # Verificar se já existe arquivo para evitar duplicação
        if caminho_arquivo.exists() and modo == "atual":
            # Para dados atuais, podemos querer atualizar o arquivo existente
            # Lê o arquivo existente
            dados_existentes = pd.read_csv(caminho_arquivo)
            
            # Se estamos lidando com INMET, temos que verificar duplicação por DATETIME
            if fonte == "inmet" and "DATETIME" in dados.columns and "DATETIME" in dados_existentes.columns:
                # Convertendo para datetime para comparação
                dados['DATETIME'] = pd.to_datetime(dados['DATETIME'])
                dados_existentes['DATETIME'] = pd.to_datetime(dados_existentes['DATETIME'])
                
                # Filtra apenas registros novos
                novos_dados = dados[~dados['DATETIME'].isin(dados_existentes['DATETIME'])]
                if not novos_dados.empty:
                    # Concatena e salva
                    dados_combinados = pd.concat([dados_existentes, novos_dados])
                    dados_combinados.to_csv(caminho_arquivo, index=False)
                    logger.info(f"Adicionados {len(novos_dados)} novos registros a {caminho_arquivo}")
                else:
                    logger.info(f"Nenhum novo registro para adicionar a {caminho_arquivo}")
            
            # Para OpenWeather, verificamos por data e hora
            elif fonte == "openweather" and "data" in dados.columns and "hora" in dados.columns:
                if "data" in dados_existentes.columns and "hora" in dados_existentes.columns:
                    # Criar chave composta para comparação
                    dados['chave_datetime'] = dados['data'] + " " + dados['hora']
                    dados_existentes['chave_datetime'] = dados_existentes['data'] + " " + dados_existentes['hora']
                    
                    # Filtra apenas registros novos
                    novos_dados = dados[~dados['chave_datetime'].isin(dados_existentes['chave_datetime'])]
                    if not novos_dados.empty:
                        # Remove a coluna auxiliar antes de salvar
                        novos_dados = novos_dados.drop('chave_datetime', axis=1)
                        dados_existentes = dados_existentes.drop('chave_datetime', axis=1)
                        
                        # Concatena e salva
                        dados_combinados = pd.concat([dados_existentes, novos_dados])
                        dados_combinados.to_csv(caminho_arquivo, index=False)
                        logger.info(f"Adicionados {len(novos_dados)} novos registros a {caminho_arquivo}")
                    else:
                        logger.info(f"Nenhum novo registro para adicionar a {caminho_arquivo}")
                else:
                    # Estrutura diferente, salva como novo arquivo
                    dados.to_csv(caminho_arquivo, index=False)
                    logger.info(f"Substituído arquivo existente {caminho_arquivo} (estrutura diferente)")
            else:
                # Caso não consiga determinar duplicação, salva como arquivo separado
                caminho_arquivo_alt = diretorio_mes / f"{modo}_{nome_regiao}_{data_str}_{int(time.time())}.csv"
                dados.to_csv(caminho_arquivo_alt, index=False)
                logger.info(f"Criado novo arquivo alternativo {caminho_arquivo_alt}")
        else:
            # Salva novo arquivo
            dados.to_csv(caminho_arquivo, index=False)
            logger.info(f"Criado novo arquivo {caminho_arquivo}")
    
    def verificar_consistencia_dados(self, dados, fonte):
        """
        Verifica a consistência dos dados coletados.
        
        Args:
            dados (pandas.DataFrame): DataFrame com os dados a serem verificados
            fonte (str): Fonte dos dados ('openweather' ou 'inmet')
            
        Returns:
            bool: True se os dados parecem consistentes, False caso contrário
        """
        if dados is None or dados.empty:
            logger.warning(f"Dados vazios de {fonte}")
            return False
        
        # Verificações gerais
        try:
            # Verificar número de colunas
            if len(dados.columns) < 5:
                logger.warning(f"Poucas colunas nos dados de {fonte}: {len(dados.columns)}")
                return False
            
            # Verificar valores missing
            percentuais_ausentes = dados.isna().mean() * 100
            alta_ausencia = percentuais_ausentes[percentuais_ausentes > 50].index.tolist()
            if alta_ausencia:
                logger.warning(f"Colunas com mais de 50% de valores ausentes em {fonte}: {alta_ausencia}")
                # Não retorna False aqui, apenas alerta
            
            # Verificações específicas por fonte
            if fonte == 'openweather':
                # Verificar se temperaturas estão em um intervalo razoável
                if 'temperatura' in dados.columns and (dados['temperatura'].min() < -40 or dados['temperatura'].max() > 55):
                    logger.warning(f"Temperaturas fora do intervalo esperado em {fonte}")
                    return False
                
                # Verificar umidade
                if 'umidade' in dados.columns and (dados['umidade'].min() < 0 or dados['umidade'].max() > 100):
                    logger.warning(f"Umidade fora do intervalo esperado em {fonte}")
                    return False
                
            elif fonte == 'inmet':
                # Verificações específicas para dados do INMET
                # As colunas exatas dependem do que é retornado pela API
                if 'TEM_INS' in dados.columns and (dados['TEM_INS'].min() < -40 or dados['TEM_INS'].max() > 55):
                    logger.warning(f"Temperaturas fora do intervalo esperado em {fonte}")
                    return False
                
                # Verificar umidade
                if 'UMD_INS' in dados.columns and (dados['UMD_INS'].min() < 0 or dados['UMD_INS'].max() > 100):
                    logger.warning(f"Umidade fora do intervalo esperado em {fonte}")
                    return False
                
            logger.info(f"Verificação de consistência concluída para {fonte} - dados parecem válidos")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar consistência dos dados de {fonte}: {e}")
            return False


def executar_coleta_atual():
    """Executa a coleta de dados atuais (últimos 7 dias)."""
    coletor = ColetorDadosClimaticos()
    coletor.coletar_para_todas_regioes(modo="atual")
    logger.info("Coleta de dados atuais concluída")


def executar_coleta_historica():
    """Executa a coleta de dados históricos (últimos 15 anos)."""
    coletor = ColetorDadosClimaticos()
    coletor.coletar_para_todas_regioes(modo="historico")
    logger.info("Coleta de dados históricos concluída")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Coletor de Dados Climáticos")
    parser.add_argument('--modo', choices=['atual', 'historico', 'ambos'], 
                        default='atual', help='Modo de coleta de dados')
    args = parser.parse_args()
    
    try:
        logger.info(f"Iniciando sistema de coleta no modo: {args.modo}")
        
        if args.modo in ('atual', 'ambos'):
            executar_coleta_atual()
        
        if args.modo in ('historico', 'ambos'):
            executar_coleta_historica()
            
        logger.info("Execução concluída com sucesso")
        
    except Exception as e:
        logger.error(f"Erro não tratado na execução: {e}")
        sys.exit(1)