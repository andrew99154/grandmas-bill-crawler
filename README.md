# 阿嬤的帳單小幫手
此專案為私人部屬於PaaS使用，公開程式碼僅作Demo用途。
## 專案結構
Procfile：供PaaS平台讀取的部屬指令文件。
billcrawlerforbot：爬蟲流程主程式。
bot.py：串接Line Messaging API、呼叫爬蟲主程式。
imageUploader：將圖片上傳至Google Cloud Storage並獲取網址。
## 技術使用
網路爬蟲：利用 Python 編寫爬蟲程式，自動獲取電子帳單資訊。
影像辨識模型：使用他人訓練的影像辨識模型，解析圖片驗證碼。
Line Bot：使用 Line Bot API 實現與使用者的互動介面。
PaaS 平台：使用 Heroku 將爬蟲程式部署在雲端，實現 Line Bot 24 小時在線。
雲端儲存空間：使用雲端儲存服務將圖片上傳以供 Line Bot API 使用。
