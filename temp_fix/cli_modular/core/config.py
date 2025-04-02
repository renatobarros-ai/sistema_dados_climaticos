"""
Gerenciamento de configuração para o Sistema de Dados Climáticos.
Centraliza acesso a configurações e credenciais.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class Config:
    """
    Gerencia configurações do sistema
    
    Attributes:
        base_dir (Path): Diretório base do sistema
        config_dir (Path): Diretório de configurações
        data_dir (Path): Diretório de dados
        logs_dir (Path): Diretório de logs
        temp_dir (Path): Diretório temporário
    """
    
    def __init__(self):
        """Inicializa o gerenciador de configurações"""
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.data_dir = self.base_dir / "dados"
        self.logs_dir = self.base_dir / "logs"
        self.temp_dir = self.base_dir / "temp"
        
        # Diretórios específicos de dados
        self.openweather_dir = self.data_dir / "openweather"
        self.inmet_dir = self.data_dir / "inmet"
        
        # Verificar e criar diretórios necessários
        self._init_directories()
        
        # Cache para configurações
        self._regioes: Optional[List[Dict[str, Any]]] = None
        self._credenciais: Optional[Dict[str, Dict[str, str]]] = None
    
    def _init_directories(self) -> None:
        """Verifica e cria os diretórios necessários se não existirem"""
        directories = [
            self.config_dir,
            self.data_dir,
            self.openweather_dir,
            self.inmet_dir,
            self.logs_dir,
            self.temp_dir
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True, parents=True)
    
    def get_regioes(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """
        Obtém as regiões configuradas
        
        Args:
            force_reload: Se True, recarrega a partir do arquivo mesmo se já em cache
            
        Returns:
            List[Dict[str, Any]]: Lista de regiões configuradas
        """
        if self._regioes is None or force_reload:
            regioes_file = self.config_dir / "regioes.json"
            
            if not regioes_file.exists():
                logger.warning(f"Arquivo de regiões não encontrado: {regioes_file}")
                self._regioes = []
                return self._regioes
            
            try:
                with open(regioes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._regioes = data.get("regioes_agricolas", [])
                    logger.info(f"Carregadas {len(self._regioes)} regiões")
            except Exception as e:
                logger.error(f"Erro ao carregar regiões: {e}")
                self._regioes = []
        
        return self._regioes
    
    def save_regioes(self, regioes: List[Dict[str, Any]]) -> bool:
        """
        Salva as regiões no arquivo de configuração
        
        Args:
            regioes: Lista de regiões a salvar
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        regioes_file = self.config_dir / "regioes.json"
        
        try:
            with open(regioes_file, "w", encoding="utf-8") as f:
                json.dump({"regioes_agricolas": regioes}, f, indent=2, ensure_ascii=False)
            
            # Atualizar cache
            self._regioes = regioes
            logger.info(f"Salvas {len(regioes)} regiões")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar regiões: {e}")
            return False
    
    def get_credenciais(self, force_reload: bool = False) -> Dict[str, Dict[str, str]]:
        """
        Obtém as credenciais configuradas
        
        Args:
            force_reload: Se True, recarrega a partir do arquivo mesmo se já em cache
            
        Returns:
            Dict[str, Dict[str, str]]: Credenciais configuradas
        """
        if self._credenciais is None or force_reload:
            credenciais_file = self.config_dir / "credenciais.json"
            
            if not credenciais_file.exists():
                logger.warning(f"Arquivo de credenciais não encontrado: {credenciais_file}")
                self._credenciais = {"openweather": {"api_key": ""}, "inmet": {"token": ""}}
                return self._credenciais
            
            try:
                with open(credenciais_file, "r", encoding="utf-8") as f:
                    self._credenciais = json.load(f)
                    logger.info("Credenciais carregadas")
            except Exception as e:
                logger.error(f"Erro ao carregar credenciais: {e}")
                self._credenciais = {"openweather": {"api_key": ""}, "inmet": {"token": ""}}
        
        return self._credenciais
    
    def save_credenciais(self, credenciais: Dict[str, Dict[str, str]]) -> bool:
        """
        Salva as credenciais no arquivo de configuração
        
        Args:
            credenciais: Credenciais a salvar
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        credenciais_file = self.config_dir / "credenciais.json"
        
        try:
            with open(credenciais_file, "w", encoding="utf-8") as f:
                json.dump(credenciais, f, indent=2, ensure_ascii=False)
            
            # Atualizar cache
            self._credenciais = credenciais
            logger.info("Credenciais salvas")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")
            return False
    
    def get_log_dir_for_current_date(self) -> Path:
        """
        Obtém o diretório de logs para a data atual
        
        Returns:
            Path: Caminho do diretório de logs para a data atual
        """
        from datetime import datetime
        
        hoje = datetime.now()
        diretorio_log_ano = self.logs_dir / str(hoje.year)
        diretorio_log_mes = diretorio_log_ano / f"{hoje.month:02d}"
        
        # Criar diretórios se não existirem
        diretorio_log_ano.mkdir(exist_ok=True, parents=True)
        diretorio_log_mes.mkdir(exist_ok=True, parents=True)
        
        return diretorio_log_mes
    
    def get_data_dir_for_current_date(self, fonte: str) -> Path:
        """
        Obtém o diretório de dados para a data atual
        
        Args:
            fonte: Nome da fonte de dados ("openweather" ou "inmet")
            
        Returns:
            Path: Caminho do diretório de dados para a data atual
        """
        from datetime import datetime
        
        hoje = datetime.now()
        
        if fonte == "openweather":
            base_dir = self.openweather_dir
        elif fonte == "inmet":
            base_dir = self.inmet_dir
        else:
            raise ValueError(f"Fonte inválida: {fonte}")
        
        diretorio_ano = base_dir / str(hoje.year)
        diretorio_mes = diretorio_ano / f"{hoje.month:02d}"
        
        # Criar diretórios se não existirem
        diretorio_ano.mkdir(exist_ok=True, parents=True)
        diretorio_mes.mkdir(exist_ok=True, parents=True)
        
        return diretorio_mes

# Instância global para acesso em todo o sistema
config = Config()