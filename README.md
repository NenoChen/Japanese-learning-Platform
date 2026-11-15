# 日々日本語 — 可部署的日文學習網站

純 HTML / CSS / JavaScript，不需要 Node 或資料庫即可使用。支援每日課程、ruby 振假名、五十音語音、單字卡、收藏、測驗、學習紀錄及本機 JSON 備份。

## 立即預覽

在本資料夾執行：

```bash
python -m http.server 8000
```

瀏覽 http://localhost:8000/ 。請勿直接雙擊 `index.html`，因為瀏覽器可能阻擋讀取 JSON。

## GitHub Pages 部署

1. 在 GitHub 建立新的公開儲存庫，例如 `hibi-japanese`。
2. 將壓縮檔解壓後的**內容**（包含隱藏的 `.github` 資料夾）上傳至儲存庫根目錄。
3. 進入 Settings → Pages → Build and deployment → Deploy from a branch，選擇 `main`、`/(root)`，儲存。
4. 等待部署後，網站網址通常是 `https://你的帳號.github.io/hibi-japanese/`。

## 每日自動同步（需額外設定資料來源）

GitHub Actions 已設置台灣時間約 06:20 每天執行，另可手動執行。它會從你提供的 HTTPS JSON feed 取得當日課程並合併進 `data/lessons.json`，依 `id` 去重。GitHub Actions 排程可能延遲，不能保證 06:20 準時。

在 GitHub 儲存庫 Settings → Secrets and variables → Actions 新增：

- `LESSON_FEED_URL`：每日講義資料的 HTTPS JSON 來源（必填）。
- `LESSON_FEED_TOKEN`：來源如需 Bearer token 才設定（選填）。

**重要**：目前的 ChatGPT 每日 PDF 排程不會自動公開 JSON feed，亦無法直接推送至 GitHub。必須另行建立「講義生成 → JSON feed」的可存取資料來源，才能真正無人值守同步。此範本提供同步接收端，但不代表這段來源已經接通。建議讓講義生成程序同時輸出 PDF 與符合下列格式的 JSON。若僅有 PDF，還需要一個 PDF 解析／校對程序，不能假定轉換完全正確。

## 教材資料格式

`data/lessons.json`：

```json
{
  "version": 1,
  "lessons": [
    {
      "id": "2026-11-16",
      "day": 4,
      "date": "2026-11-16",
      "title": "今日の勉強",
      "level": "N5",
      "articles": [
        {
          "title": "朝の生活",
          "category": "基礎閱讀",
          "sentences": [
            {"html": "<ruby>今日<rt>きょう</rt></ruby>はいい<ruby>天気<rt>てんき</rt></ruby>です。", "zh": "今天天氣很好。"}
          ]
        }
      ],
      "words": [{"id":"w1","jp":"今日","reading":"きょう","meaning":"今天","pos":"名詞"}],
      "grammar": [{"pattern":"～です","meaning":"禮貌判斷句","example":"いい天気です。"}],
      "quiz": [{"q":"今日的日文是？","options":["きょう","あした"],"answer":0,"explanation":"今日＝きょう。"}]
    }
  ]
}
```

來源也可直接提供單筆課程物件。`sentences[].html` 只允許純文字及 `<ruby>` / `<rt>` 標記；請不要放任何其他 HTML。

## 資料保存與限制

- 單字收藏、測驗成績及完成紀錄使用瀏覽器 localStorage，不會跨裝置自動同步；可從「學習紀錄」匯出／匯入備份。
- 五十音朗讀使用瀏覽器內建 Web Speech API，發音品質取決於裝置是否有日語語音。
- 範例 Day 03 為**示範教材**，非你先前 PDF 的逐字匯入；新聞段落也不是已查證新聞。
- 網站為靜態站點，無登入、雲端帳號同步或 PDF 解析服務；未配置 feed 時仍可使用內建示範課程。
- GitHub Pages 公開站點上的教材 JSON 任何人都可讀取，勿放個人敏感資料或秘密金鑰。

## 手機 PWA 安裝與離線

網站已包含 `manifest.webmanifest`、`sw.js` 與 192/512px 圖示。請部署至 HTTPS（GitHub Pages 即可），首次連網載入後，Service Worker 會快取網站與 `data/lessons.json`；後續離線可閱讀已快取課程。教材在連線時採網路優先更新，離線時讀取快取。注意：尚未快取的新課程無法離線使用；語音朗讀依賴裝置語音引擎，未必可離線運作。

- iPhone Safari：分享 → 加入主畫面。
- Android Chrome：選單 → 安裝應用程式／加到主畫面。
- `localhost` 可測試 PWA；直接用 `file://` 開啟無法註冊 Service Worker。
- 目前學習紀錄使用 localStorage，只保存在同一裝置及網站來源，清除網站資料可能遺失，請定期匯出備份。


## 2026-11-15 教材更新

已整合 Day 01–03 每天五篇日文文章、中文全文翻譯、核心單字、文法、系列單字及測驗；並附原始 PDF 供核對。Day 02 綜合測驗為從 PDF 的系列與閱讀題選錄，非 PDF 原本綜合十題的逐題重製。原始 PDF 的逐篇補充單字、解析與全部練習仍以 PDF 為準。網站未連接 ChatGPT 自動推送。
