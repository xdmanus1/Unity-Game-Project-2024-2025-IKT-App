
# 🚀 Game Launcher with Firebase Integration 🎮

A sleek game launcher app built using **PyQt6** and **Firebase**! This launcher allows users to download and play the latest version of a game directly from Firebase Storage. The app includes animated buttons, real-time download progress, and a toggleable dev mode for advanced testing.

## ✨ Features
- 🔗 **Firebase Integration**: 
  - Fetches the latest game version and downloads updates using **Firebase Realtime Database** and **Firebase Storage**.
- 📥 **Download Manager**: 
  - Tracks real-time progress of your downloads, including download speed and total file size.
- 🗜️ **Zip File Handling**: 
  - Automatically extracts downloaded `.zip` files to ensure smooth gameplay.
- 🎮 **Run Game**: 
  - Once downloaded, easily launch your game from within the app.
- 📊 **Progress Bar**: 
  - Shows detailed download progress, with an option to cancel mid-download.
- 🛠️ **Dev Mode**: 
  - Toggle dev mode for advanced testing and debugging features.
- 🖱️ **Animated UI**: 
  - Sleek, interactive UI with hover animations on buttons for a polished look.

## 🛠️ Setup & Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/xdmanus1/Unity-Game-Project-2024-2025-IKT-App.git
    ```

2. **Configure Firebase**: 
   - Replace the Firebase configuration in the code with your own Firebase project details.

3. **Run the application**:
    ```bash
    python launcher.py
    ```

## ⚙️ Firebase Configuration
Make sure you set up a Firebase project and update the Firebase credentials in the `config` dictionary to match your project’s API keys and storage settings.

```python
config = {
    "apiKey": "<YOUR_API_KEY>",
    "authDomain": "<YOUR_AUTH_DOMAIN>",
    "databaseURL": "<YOUR_DATABASE_URL>",
    "projectId": "<YOUR_PROJECT_ID>",
    "storageBucket": "<YOUR_STORAGE_BUCKET>",
    "messagingSenderId": "<YOUR_MESSAGING_SENDER_ID>",
    "appId": "<YOUR_APP_ID>"
}
```

## 🧰 Requirements
- **Python 3.x**
- **PyQt6**
- **Requests**
- **Pyrebase**
- **Zipfile**
- **Subprocess**


## 🚨 Usage
- **Download Latest Update**: Click the "Download Latest Update" button to start downloading the latest game version from Firebase.
- **Run Game**: Once the download completes, click "Run Game" to launch the game.
- **Dev Mode**: Hidden feature for developers—enable it to access additional debugging options.

## 📝 License
This project is licensed under the **MIT License**. Feel free to fork, contribute, or report any issues!

---

Made with ❤️ by xdmanus(https://github.com/xdmanus1)
