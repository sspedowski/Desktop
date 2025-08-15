import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ConfirmationDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
}

interface ConfirmationContextType {
  showConfirmation: (title: string, message: string) => Promise<boolean>;
}

const ConfirmationContext = createContext<ConfirmationContextType | undefined>(undefined);

export function ConfirmationProvider({ children }: { children: ReactNode }) {
  const [dialog, setDialog] = useState<ConfirmationDialogProps | null>(null);
  const [resolveRef, setResolveRef] = useState<((value: boolean) => void) | null>(null);

  const showConfirmation = (title: string, message: string): Promise<boolean> => {
    return new Promise((resolve) => {
      setDialog({ isOpen: true, title, message });
      setResolveRef(() => resolve);
    });
  };

  const handleConfirm = () => {
    resolveRef?.(true);
    setDialog(null);
    setResolveRef(null);
  };

  const handleCancel = () => {
    resolveRef?.(false);
    setDialog(null);
    setResolveRef(null);
  };

  return (
    <ConfirmationContext.Provider value={{ showConfirmation }}>
      {children}
      {dialog && dialog.isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-semibold mb-2">{dialog.title}</h2>
            <p className="text-neutral-600 mb-6">{dialog.message}</p>
            <div className="flex justify-end gap-3">
              <button onClick={handleCancel} className="px-4 py-2 rounded-xl border hover:bg-neutral-50">
                Cancel
              </button>
              <button onClick={handleConfirm} className="px-4 py-2 rounded-xl bg-black text-white hover:bg-neutral-800">
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </ConfirmationContext.Provider>
  );
}

export function useConfirmation() {
  const context = useContext(ConfirmationContext);
  if (!context) {
    throw new Error('useConfirmation must be used within a ConfirmationProvider');
  }
  return context;
}
