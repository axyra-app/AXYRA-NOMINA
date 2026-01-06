import React from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = ({ id, message, type, onClose }) => {
  React.useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const bgColor = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    warning: 'bg-yellow-50 border-yellow-200',
    info: 'bg-blue-50 border-blue-200',
  }[type] || 'bg-blue-50 border-blue-200';

  const textColor = {
    success: 'text-green-800',
    error: 'text-red-800',
    warning: 'text-yellow-800',
    info: 'text-blue-800',
  }[type] || 'text-blue-800';

  const Icon = {
    success: CheckCircle,
    error: AlertCircle,
    warning: AlertCircle,
    info: Info,
  }[type] || Info;

  const iconColor = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
  }[type] || 'text-blue-600';

  return (
    <div className={`${bgColor} border rounded-lg p-4 flex items-start gap-3 mb-3 shadow-md animate-slideIn`}>
      <Icon className={`${iconColor} flex-shrink-0 mt-0.5`} size={20} />
      <p className={`${textColor} flex-1`}>{message}</p>
      <button
        onClick={onClose}
        className={`${textColor} opacity-50 hover:opacity-100 transition-opacity flex-shrink-0`}
        aria-label="Cerrar notificación"
      >
        <X size={18} />
      </button>
    </div>
  );
};

export const ToastContainer = ({ notifications, onClose }) => {
  return (
    <div className="fixed bottom-4 right-4 max-w-sm z-50 pointer-events-auto">
      {notifications.map((notification) => (
        <Toast
          key={notification.id}
          id={notification.id}
          message={notification.message}
          type={notification.type}
          onClose={() => onClose(notification.id)}
        />
      ))}
    </div>
  );
};

export default Toast;
