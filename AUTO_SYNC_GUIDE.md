# 日々日本語：PDF 與網站教材一致的同步方案

## 最重要的限制
ChatGPT 排程產生的附件不會自動出現在 GitHub Actions、GitHub 儲存庫或其他雲端資料夾。**本專案無法自行取得 ChatGPT 排程的 PDF**，因此在未設定具有權限的外部傳送端前，不能宣稱「每天 06:00 全自動同步」已啟用。

而且 PDF 本身通常無法可靠還原振假名位置、題目答案、文章對應、完整單字結構。要達成「PDF 與網站完全一致」，請讓**同一次教材生成**同時產出 PDF 與 `lesson.json`，並對兩者做內容核對。不要讓網站獨立生成第二份不同的教材。

## 已實作
- 保留 Day 01–03 網站、PWA、原 PDF、單字收藏與學習紀錄。
- GitHub Actions：有新的 `incoming/YYYY-MM-DD/manifest.json` 時，驗證 PDF/JSON SHA-256、日期、課程欄位、Ruby 標記與測驗答案；通過後匯入 `data/lessons.json` 與 `materials/DayXX.pdf`，自動 commit，觸發 Pages 重新部署。
- `scripts/create_bundle.py`：將同一次生成的 PDF 與 JSON 包成有 SHA-256 校驗的三檔資料包。
- `scripts/push_bundle_github.py`：提供可由外部可信任排程執行的 GitHub API 上傳程式。**必須在可信任的服務器/電腦執行，不可把 Token 放到公開網站或前端程式**。
- 更新後的 PWA 連網讀取新 `data/lessons.json`；離線可使用已快取內容。

## 一次性部署
1. 備份現有 GitHub 儲存庫。下載 ZIP，解壓縮，將**內容**上傳至儲存庫根目錄（包含隱藏 `.github/workflows/import-daily-pdf.yml`）。網頁版拖曳上傳可能漏掉隱藏資料夾，請用 GitHub 網頁「Add file → Create new file」手動建立 `.github/workflows/import-daily-pdf.yml`，貼上本檔內容；或使用 Git CLI 推送整個目錄。
2. GitHub → Settings → Actions → General → Workflow permissions：允許 **Read and write permissions**（若組織政策允許）。
3. GitHub → Settings → Pages：維持 `main` / `/(root)`。檢查 Actions 工作流程是否出現 `Import verified daily PDF and lesson`。
4. 手機 PWA 打開一次新網址以更新快取，確認 Day 01–03 正常。

## 每日來源設定：嚴格一致模式
**必要前提**：能取得當天 ChatGPT PDF 的可信任傳送端，並同時取得同一份講義對應的結構化 JSON。

- 建議修改 ChatGPT 每日講義排程，要求「先產生單一結構化教材來源，據此渲染 PDF；同時輸出相同來源的 lesson.json；不得各自重新生成」。這會改善一致性，但**不會自動把排程附件傳出 ChatGPT**。
- 若 ChatGPT 排程無法向外傳檔，請使用有授權的外部工作流程/雲端電腦，從可存取的來源取得 PDF 與 JSON，執行下列命令。沒有外部傳送端時，仍須手動上傳三個檔案。
- 自動化傳送端必須以固定日期核對 PDF 與 JSON；發生衝突時流程拒絕覆寫既有課程。

## 製作與上傳資料包
同一次產出的 `lesson.pdf` 和 `lesson.json`（後者必須符合 `data/lessons.json` 中單筆課程的結構）放在可信任電腦，執行：

```bash
python scripts/create_bundle.py --pdf lesson.pdf --json lesson.json
```

會得到 `incoming/2026-11-16/lesson.pdf`、`lesson.json`、`manifest.json`。日期以 JSON 的 `date` 為準。

**不使用 Token 的手動路徑**：在 GitHub 儲存庫內建立 `incoming/YYYY-MM-DD/`，依序上傳 `lesson.pdf`、`lesson.json`，**最後才上傳** `manifest.json`；Actions 將自動匯入並部署。這是安全的備援流程，不是全自動。

**有授權的自動路徑**：在可信任執行環境設定 `GH_TOKEN`（fine-grained PAT，僅授權該儲存庫 Contents: Read and write），執行：

```bash
python scripts/push_bundle_github.py --folder incoming/2026-11-16 --repo NenoChen/Japanese-learning-Platform
```

該程式依序上傳 PDF、JSON、最後 manifest 以觸發驗證。Token 只能放在外部執行環境的 Secret 中，不能提交 GitHub、放在公開 HTML 或分享給聊天對話。

## JSON 結構
`lesson.json` 是一個**單筆課程物件**，參照 `data/lessons.json` 中的任何一筆，例如包含：

```json
{
  "id": "2026-11-16",
  "date": "2026-11-16",
  "day": 4,
  "title": "當日標題",
  "level": "N5",
  "articles": [{"title":"文章標題","category":"基礎閱讀","sentences":[{"html":"<ruby>今日<rt>きょう</rt></ruby>は晴れです。","zh":"今天天氣晴朗。"}],"note":""}],
  "words": [{"id":"w1","jp":"今日","reading":"きょう","pos":"名詞","meaning":"今天"}],
  "grammar": [{"pattern":"～です","meaning":"是……","example":"学生です。"}],
  "quiz": [{"q":"今日の天気は？","options":["晴れ","雨"],"answer":0,"explanation":"文章說明今天是晴天。"}]
}
```

若有星期、時間、日期系列，沿用既有 `series` 欄位格式。**上述內容僅為格式範例，不能當成實際 Day 04 教材**。

## 如何確認成功
- GitHub → Actions → `Import verified daily PDF and lesson` → 綠色完成。
- 儲存庫 `data/lessons.json` 新增當天 `id`；`materials/Day04.pdf` 與來源 PDF SHA-256 一致。
- GitHub Pages 完成重新部署後，在手機 PWA 連網開啟並重新載入。
- 若驗證失敗，檢查 Actions log；不會靜默產生與 PDF 不同的教材。

## 尚未完成的最後一哩
**必須另外設定能從 ChatGPT 排程取得附件的外部傳送端**。如果目前 ChatGPT 排程沒有提供可讀取附件的 API/連接器，就無法直接無人值守完成方案 A。此 ZIP 提供已可運作的 GitHub 接收端、驗證端及可供外部傳送端呼叫的上傳工具；沒有聲稱已連接 ChatGPT。
