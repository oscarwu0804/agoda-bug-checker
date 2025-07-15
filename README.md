
# Agoda Bug 價檢測器 - Railway 版

## 📄 說明
自動檢查 Agoda 全球（非非洲）未來一年內房價，找出低於均價 50% 且不是 Hostel/Capsule 的疑似 Bug 價，並透過 Gmail 通知。

## 🚀 部署到 Railway
1. 註冊帳號 https://railway.app/
2. 點擊「New Project」→「Deploy from GitHub or ZIP」
3. 上傳此專案 ZIP
4. Railway 會自動偵測 `Procfile` 建立 Worker 服務
5. 在「Variables」設定 Gmail 帳號、密碼等
6. 點擊「Deploy」，部署完成後會 24 小時執行

## ⚙️ 設定
- `config.py` 可修改城市與 Gmail 帳號
- 每 30 分鐘檢查一次
