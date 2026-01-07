"""
📊 SISTEMA AVANZADO DE LOGGING
Logging estructurado con JSON para análisis y monitoreo
"""

import logging
import logging.handlers
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from app.config.settings import settings


class JSONFormatter(logging.Formatter):
    """Formateador que produce logs en JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar información adicional si existe
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        # Agregar excepción si existe
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }
        
        return json.dumps(log_data, ensure_ascii=False)


class PlainFormatter(logging.Formatter):
    """Formateador legible para consola"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record: logging.LogRecord) -> str:
        if sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            
            prefix = {
                'DEBUG': '🔍',
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '[ERROR]',
                'CRITICAL': '🚨'
            }.get(record.levelname, '•')
            
            return (
                f"{color}{prefix} {datetime.fromtimestamp(record.created).strftime('%H:%M:%S')} "
                f"[{record.name}] {record.getMessage()}{reset}"
            )
        else:
            return (
                f"{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')} "
                f"[{record.levelname:8s}] {record.name}: {record.getMessage()}"
            )


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Handler con rotación diaria y tamaño"""
    
    def __init__(self, filename: str, maxBytes: int = 10485760, backupCount: int = 10):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount)


def setup_logging():
    """Configura el sistema de logging profesional"""
    
    # Configuración base
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    
    # Logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # ===== CONSOLE HANDLER =====
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if settings.LOG_FORMAT == "json":
        console_formatter = JSONFormatter()
    else:
        console_formatter = PlainFormatter()
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # ===== FILE HANDLER (JSON) =====
    if settings.LOG_FILE:
        try:
            file_handler = RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=10
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(JSONFormatter())
            root_logger.addHandler(file_handler)
            
            logging.getLogger(__name__).info(
                f"[OK] Log file configured: {settings.LOG_FILE}"
            )
        except Exception as e:
            logging.getLogger(__name__).warning(
                f"⚠️  No se pudo crear archivo de log: {str(e)}"
            )
    
    # ===== ERROR FILE HANDLER (Errores solamente) =====
    error_log = "logs/errors.log"
    try:
        error_handler = RotatingFileHandler(
            error_log,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(error_handler)
    except Exception as e:
        logging.getLogger(__name__).warning(
            f"⚠️  No se pudo crear archivo de errores: {str(e)}"
        )
    
    # Configurar loggers específicos
    setup_module_loggers()
    
    logging.info("[OK] Logging system initialized")


def setup_module_loggers():
    """Configura loggers para módulos específicos"""
    
    # Reducir verbosidad de librerías externas
    logging.getLogger("firebase_admin").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # Nuestros módulos en DEBUG/INFO
    logging.getLogger("app").setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


class ContextualLogger:
    """Logger que mantiene contexto a través de la aplicación"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context = {}
    
    def set_context(self, **kwargs):
        """Establece contexto"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Limpia contexto"""
        self.context.clear()
    
    def _log_with_context(self, level: str, message: str, **extra_data):
        """Log con contexto"""
        context_data = self.context.copy()
        context_data.update(extra_data)
        
        log_record = logging.LogRecord(
            name=self.logger.name,
            level=getattr(logging, level),
            pathname="",
            lineno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        log_record.extra_data = context_data
        
        getattr(self.logger, level.lower())(message)
    
    def info(self, message: str, **extra_data):
        self._log_with_context("INFO", message, **extra_data)
    
    def debug(self, message: str, **extra_data):
        self._log_with_context("DEBUG", message, **extra_data)
    
    def warning(self, message: str, **extra_data):
        self._log_with_context("WARNING", message, **extra_data)
    
    def error(self, message: str, **extra_data):
        self._log_with_context("ERROR", message, **extra_data)
    
    def critical(self, message: str, **extra_data):
        self._log_with_context("CRITICAL", message, **extra_data)


# Instancia global para uso
logger = logging.getLogger(__name__)


def get_contextual_logger(name: str) -> ContextualLogger:
    """Obtiene logger contextual"""
    return ContextualLogger(name)
