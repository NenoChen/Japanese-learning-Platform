# 每日 PDF 半自動匯入（安全版）

## 已有功能

- `Review uploaded Japanese lesson PDF`：上傳 `pdf-inbox/YYYY-MM-DD.pdf` 後，自動擷取 PDF 文字並提供 Actions Artifact `japanese-pdf-review`。**不會直接發佈**，因為 PDF 文字抽取不能保證還原 ruby 振假名、單字讀音、測驗正確答案與所有結構化欄位。
- `Import verified daily PDF and lesson`：收到 `incoming/YYYY-MM-DD/lesson.pdf`、`lesson.json`、`manifest.json` 三個經驗證檔案後，會驗證雜湊、更新課程及 PDF，並自動產生 MP3。這次已把 MP3 生成整合進匯入 Workflow，不必再手動啟動 MP3 工作流程。

## 每天建議的操作（目前最可靠）

1. 下載 ChatGPT 當日 PDF，並上傳到 ChatGPT 對話，要求根據 PDF 建立與內容一致的 `lesson.json` 和完整匯入 ZIP。
2. 下載產生的匯入 ZIP，將 `incoming/YYYY-MM-DD/` 的三個檔案上傳至 GitHub 相同路徑（務必一併上傳 manifest.json）。
3. GitHub Actions 自動驗證並匯入，生成 MP3，更新 GitHub Pages。若 GitHub Actions 顯示失敗，查看錯誤訊息；不要略過驗證。

## 只想先把 PDF 放進 GitHub？

1. 在 GitHub 建立 `pdf-inbox/2026-11-16.pdf` 這類日期命名的 PDF。
2. 進入 Actions → `Review uploaded Japanese lesson PDF` → 該次執行，下載 `japanese-pdf-review` Artifact。
3. 擷取文字是供人工／ChatGPT 核對的草稿，不是可直接匯入網站的完整 JSON。

## 注意

- 「只上傳 PDF 即完全自動、準確轉成完整課程」尚未實現。PDF 本身不是結構化教材的可靠來源，尤其是日文 ruby、測驗與單字欄位。
- 原本 MP3 朗讀、個人單字本、五十音及 PWA 前端保持不變。
- GitHub Actions 的 `contents: write` 權限與 repository Actions 設定必須允許 workflow 提交檔案。
