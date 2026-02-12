import React from 'react';
import clsx from 'clsx';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Modal = ({
  isOpen = false,
  onClose = () => {},
  title = '',
  children,
  footer = null,
  size = 'md',
  closeOnBackdropClick = true,
  closeButton = true,
  className = '',
}) => {
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    'full': 'max-w-4xl',
  };

  const handleBackdropClick = (e) => {
    if (closeOnBackdropClick && e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-backdrop"
            onClick={handleBackdropClick}
          />
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="fixed inset-0 flex items-center justify-center z-50 p-4"
          >
            <div
              className={clsx(
                'card-base w-full',
                sizeClasses[size] || sizeClasses.md,
                className
              )}
            >
              {/* Header */}
              {title && (
                <div className="flex items-center justify-between px-6 py-4 border-b border-simplyfi-border-light">
                  <h2 className="text-xl font-semibold text-simplyfi-text-dark">{title}</h2>
                  {closeButton && (
                    <button
                      onClick={onClose}
                      className="p-1 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                    >
                      <X className="w-5 h-5 text-simplyfi-text-muted" />
                    </button>
                  )}
                </div>
              )}

              {/* Content */}
              <div className="px-6 py-4 max-h-[calc(100vh-200px)] overflow-y-auto">{children}</div>

              {/* Footer */}
              {footer && (
                <div className="px-6 py-4 border-t border-simplyfi-border-light flex items-center justify-end gap-3">
                  {footer}
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default Modal;
