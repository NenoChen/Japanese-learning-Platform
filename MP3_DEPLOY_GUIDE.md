# 日々日本語｜預先產生 MP3 朗讀版

## 這一包的狀態

網站程式與 GitHub Actions 已加入 MP3 支援，但 **ZIP 內尚未包含實際 MP3**，因為目前建置環境無法連線至語音服務。首次上傳後，請在 GitHub Actions 執行 **Generate Japanese MP3 library**，GitHub Runner 會透過 gTTS 產生真正的 MP3，並將檔案提交到 `audio/`。這是一次性的初始化操作。

## 部署

1. 將本 ZIP 的 `Japanese-learning-Platform-main` 內所有檔案和隱藏 `.github` 資料夾上傳到 GitHub 儲存庫根目錄，覆蓋同名檔案。
2. GitHub → Actions → `Generate Japanese MP3 library` → Run workflow → main → Run workflow。
3. 等待綠色勾勾，並檢查 `audio/` 出現多個 `.mp3` 與 `index.json`。
4. 開啟網站，選 Day 01–03，按全文朗讀或單字喇叭。手機 PWA 重新整理或關閉重開以更新。
5. 未來新的 PDF+JSON 經 `Import verified daily PDF and lesson` 匯入時，該流程會同步產生新 MP3 並提交 GitHub。注意：ChatGPT 排程 PDF 的外部傳輸尚未接通，仍需另行解決。

## 播放與離線

文章、段落、單字、單字本、五十音都優先使用預先產生的 MP3。語速可在 0.75–1.25 倍間調整；不會把 ruby 振假名讀兩次。網站採用播放過的音檔逐步快取；**未曾播放過的 MP3 不保證離線可用**。缺少 MP3 時暫時退回瀏覽器 TTS。

## 技術與注意事項

- 使用 gTTS（非官方 Google Translate TTS 介面）在 GitHub Runner 連線生成音檔。服務可能限流、拒絕請求或變更；發生時工作流程會失敗，並不會默默宣稱完成。
- 這些 MP3 由網站 JSON 原文產生，不保證語音模型對每個漢字的讀法完全正確；請抽查多音字、人名、數字和日期。
- `audio/index.json` 使用日文文字對應 MP3 相對路徑；更換教材後重新執行生成工作流程即可補齊。
- 公開 GitHub Pages 會公開 MP3 與教材檔案。生成大量單字音檔可能增加儲存庫大小。
- 如果 GitHub Actions 沒有寫入權限：Settings → Actions → General → Workflow permissions → Read and write permissions。
