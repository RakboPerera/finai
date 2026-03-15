'use client';
import { useState, useCallback } from 'react';
import TopBar from '@/components/layout/TopBar';
import Button from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Loading';
import { api } from '@/lib/api';
import { Upload, FileSpreadsheet, CheckCircle2, AlertCircle, Trash2, Eye } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useEffect } from 'react';

export default function UploadPage() {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState('');
  const [uploads, setUploads] = useState<any[]>([]);
  const [selectedPreview, setSelectedPreview] = useState<any>(null);

  const loadUploads = useCallback(() => {
    api.getUploads().then((res) => setUploads(res.data || [])).catch(() => {});
  }, []);

  useEffect(() => { loadUploads(); }, [loadUploads]);

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError('');
    setUploadResult(null);
    try {
      const res = await api.uploadFile(file);
      setUploadResult(res.data);
      loadUploads();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleUpload(file);
  }, []);

  const onFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  };

  const handlePreview = async (uploadId: string) => {
    try {
      const res = await api.getUpload(uploadId);
      setSelectedPreview(res.data);
    } catch { }
  };

  return (
    <div>
      <TopBar title="Upload Data" />
      <div className="p-6 space-y-6">
        {/* Dropzone */}
        <div
          className={cn('dropzone p-12 text-center cursor-pointer rounded-xl transition-all', dragActive && 'active')}
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={onDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input id="file-input" type="file" accept=".xlsx,.xls,.csv" className="hidden" onChange={onFileSelect} />
          {uploading ? (
            <div className="flex flex-col items-center gap-3">
              <Spinner size="lg" />
              <p className="text-sm text-fin-accent">Processing your file...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-3">
              <div className="w-16 h-16 rounded-2xl bg-fin-accent/10 flex items-center justify-center">
                <Upload className="w-8 h-8 text-fin-accent" />
              </div>
              <div>
                <p className="text-base font-semibold text-fin-text">Drop your SAP Excel file here</p>
                <p className="text-sm text-fin-muted mt-1">Supports .xlsx, .xls, .csv files</p>
              </div>
              <Button variant="secondary" size="sm">Browse Files</Button>
            </div>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="glass-card p-4 border-fin-danger/30 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-fin-danger" />
            <p className="text-sm text-fin-danger">{error}</p>
          </div>
        )}

        {/* Upload Result */}
        {uploadResult && (
          <div className="glass-card p-5 border-fin-success/20 animate-slide-up">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle2 className="w-5 h-5 text-fin-success" />
              <h3 className="text-sm font-semibold text-fin-success">File Processed Successfully</h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div><p className="text-fin-muted text-xs">Filename</p><p className="text-fin-text font-medium">{uploadResult.filename}</p></div>
              <div><p className="text-fin-muted text-xs">Sheets</p><p className="text-fin-text font-medium">{uploadResult.sheets}</p></div>
              <div><p className="text-fin-muted text-xs">Total Rows</p><p className="text-fin-text font-medium">{uploadResult.total_rows?.toLocaleString()}</p></div>
              <div><p className="text-fin-muted text-xs">Upload ID</p><p className="text-fin-accent font-mono text-xs">{uploadResult.upload_id}</p></div>
            </div>
            {uploadResult.columns && (
              <div className="mt-4">
                <p className="text-xs text-fin-muted mb-2">Columns Detected</p>
                <div className="flex flex-wrap gap-1.5">
                  {Object.entries(uploadResult.columns).map(([sheet, cols]: any) =>
                    cols.map((col: string) => (
                      <span key={`${sheet}-${col}`} className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-fin-accent/10 text-fin-accent border border-fin-accent/20">
                        {col}
                      </span>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Uploads List */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-fin-text mb-4">Uploaded Files</h3>
          {uploads.length === 0 ? (
            <p className="text-sm text-fin-muted py-6 text-center">No files uploaded yet</p>
          ) : (
            <div className="space-y-2">
              {uploads.map((u: any) => (
                <div key={u.upload_id || u._id} className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30 hover:border-fin-accent/20 transition-colors">
                  <div className="flex items-center gap-3">
                    <FileSpreadsheet className="w-5 h-5 text-fin-success" />
                    <div>
                      <p className="text-sm text-fin-text font-medium">{u.filename}</p>
                      <p className="text-xs text-fin-muted">{u.total_rows} rows • ID: {u.upload_id}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button onClick={() => handlePreview(u.upload_id)} className="p-1.5 rounded-md hover:bg-fin-hover text-fin-muted hover:text-fin-accent transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button onClick={() => { api.deleteUpload(u.upload_id).then(loadUploads); }} className="p-1.5 rounded-md hover:bg-fin-hover text-fin-muted hover:text-fin-danger transition-colors">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Data Preview */}
        {selectedPreview && (
          <div className="glass-card p-5 animate-slide-up">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-fin-text">Data Preview</h3>
              <button onClick={() => setSelectedPreview(null)} className="text-xs text-fin-muted hover:text-fin-text">Close</button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-fin-border">
                    {selectedPreview.preview?.slice(0, 1).map((row: any) =>
                      Object.keys(row).slice(0, 8).map((key) => (
                        <th key={key} className="text-left py-2 px-3 text-fin-muted font-medium whitespace-nowrap">{key}</th>
                      ))
                    )}
                  </tr>
                </thead>
                <tbody>
                  {selectedPreview.preview?.slice(0, 20).map((row: any, i: number) => (
                    <tr key={i} className="border-b border-fin-border/30 hover:bg-fin-hover/30">
                      {Object.values(row).slice(0, 8).map((val: any, j: number) => (
                        <td key={j} className="py-2 px-3 text-fin-text whitespace-nowrap">{String(val).slice(0, 30)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
