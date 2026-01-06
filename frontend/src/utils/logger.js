/**
 * Logger utility para logging consistente en el frontend
 */

const LogLevel = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

class Logger {
  constructor(namespace = 'App') {
    this.namespace = namespace;
    this.isDevelopment = process.env.NODE_ENV === 'development';
  }

  private formatMessage(level, message, data) {
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] [${this.namespace}] [${level}]`;
    
    if (data) {
      return `${prefix} ${message}:`, data;
    }
    return `${prefix} ${message}`;
  }

  debug(message, data) {
    if (this.isDevelopment) {
      console.debug(this.formatMessage(LogLevel.DEBUG, message, data), data || '');
    }
  }

  info(message, data) {
    console.log(this.formatMessage(LogLevel.INFO, message, data), data || '');
  }

  warn(message, data) {
    console.warn(this.formatMessage(LogLevel.WARN, message, data), data || '');
  }

  error(message, error) {
    console.error(this.formatMessage(LogLevel.ERROR, message, true), error || '');
    
    // Enviar a servicio de logging remoto en producción (opcional)
    if (!this.isDevelopment) {
      this.sendToRemoteLogger(LogLevel.ERROR, message, error);
    }
  }

  private sendToRemoteLogger(level, message, error) {
    // Implementar si es necesario enviar logs a un servicio remoto
    // Ejemplo: Sentry, LogRocket, etc.
  }
}

// Crear instancias por módulo
export const createLogger = (namespace) => new Logger(namespace);

export default Logger;
