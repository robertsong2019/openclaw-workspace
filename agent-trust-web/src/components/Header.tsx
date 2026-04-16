import React from 'react';

interface HeaderProps {
  onExport?: () => void;
  onImport?: (data: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ onExport, onImport }) => {
  const handleExport = () => {
    onExport?.();
  };

  const handleImport = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        onImport?.(content);
      };
      reader.readAsText(file);
    }
  };

  return (
    <header className="bg-[#161b22] border-b border-[#30363d] h-12 flex items-center px-4 gap-4">
      <h1 className="text-base font-semibold text-[#58a6ff]">🧪 Agent Trust Network</h1>
      <span className="bg-[#58a6ff] text-[#0d1117] px-2 py-0.5 rounded-full text-xs font-semibold">
        PageRank
      </span>
      <div className="ml-auto flex gap-2">
        <label className="btn btn-secondary text-xs cursor-pointer">
          Import
          <input
            type="file"
            accept=".json"
            onChange={handleImport}
            className="hidden"
          />
        </label>
        <button className="btn btn-secondary text-xs" onClick={handleExport}>
          Export
        </button>
      </div>
    </header>
  );
};
