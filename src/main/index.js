const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            enableRemoteModule: false,
            webSecurity: false,
        }
    });

    mainWindow.loadURL('http://localhost:8080');
    mainWindow.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

ipcMain.on('save-file', async (event, { buffer, filename }) => {
    if (!filename.toLowerCase().endsWith('.bat')) {
        filename += '.bat';
    }

    const downloadPath = path.join(app.getPath('downloads'), filename);

    fs.writeFile(downloadPath, Buffer.from(buffer), (err) => {
        if (err) {
            console.error('Error saving file:', err);
            event.reply('save-file-error', err.message);
        } else {
            console.log('File saved successfully:', downloadPath);
            event.reply('save-file-complete', { path: downloadPath });
        }
    });
});

ipcMain.on('run-file', (event, filePath) => {
    console.log('Attempting to run file:', filePath);

    if (!fs.existsSync(filePath)) {
        console.error('File does not exist:', filePath);
        event.reply('run-file-error', 'File does not exist');
        return;
    }

    const command = `cmd.exe /c start "" "${filePath}"`;
    console.log('Executing command:', command);

    exec(command, { windowsHide: true }, (error, stdout, stderr) => {
        if (error) {
            console.error('Error running file:', error);
            event.reply('run-file-error', error.message);
            return;
        }
        if (stderr) {
            console.error('stderr:', stderr);
            event.reply('run-file-error', stderr);
            return;
        }
        console.log('File executed successfully');
        console.log('stdout:', stdout);
        event.reply('run-file-complete', stdout);
    });
});