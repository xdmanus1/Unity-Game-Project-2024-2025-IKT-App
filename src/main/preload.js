// preload.js
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    saveFile: (buffer, filename) => ipcRenderer.send('save-file', { buffer, filename }),
    runFile: (filePath) => ipcRenderer.send('run-file', filePath),
    onSaveFileComplete: (callback) => ipcRenderer.on('save-file-complete', callback),
    onSaveFileError: (callback) => ipcRenderer.on('save-file-error', callback),
    onRunFileComplete: (callback) => ipcRenderer.on('run-file-complete', callback),
    onRunFileError: (callback) => ipcRenderer.on('run-file-error', callback),
})