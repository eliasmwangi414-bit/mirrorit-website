const { app, BrowserWindow } = require('electron');
const path = require('path');

// 1. Start the Express server
require('./server.js');

let mainWindow;

function createWindow() {
  // 2. Create the browser window for the Admin Dashboard
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(__dirname, 'images', 'logo_icon.svg'), // Use existing logo
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // Hide the default Electron menu bar for a native app feel
  mainWindow.setMenuBarVisibility(false);

  // 3. Load the local admin login page
  // We wait a brief moment to ensure the Express server is fully bound to the port
  setTimeout(() => {
    mainWindow.loadURL('http://localhost:3005/admin-login');
  }, 500);

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});
