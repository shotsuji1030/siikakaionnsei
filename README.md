# 詩歌会 展示音声ガイド

アップロードした案内音声を再生し、間隔を空けてループ再生する Streamlit アプリです。

## ファイル

- `app.py` — Streamlit アプリ
- `guide.mp3` — 案内音声
- `requirements.txt` — 依存パッケージ

## ローカル実行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud へ公開

1. GitHub に新しいリポジトリ（例：`shikakai-audio-guide`）を作る。
2. このフォルダの **3ファイル**（`app.py`, `guide.mp3`, `requirements.txt`）をリポジトリのルートにアップロードする。
3. https://share.streamlit.io/ に GitHub アカウントでログインし、Create app を押す。
4. リポジトリ、ブランチ `main`、エントリーファイル `app.py` を指定して Deploy を押す。
5. 生成された `*.streamlit.app` のURLにアクセスする。

**注**：ブラウザの自動再生制限のため最初の1回はユーザーが再生ボタンを押してください。ページを開いたままにすれば設定した間隔でループ再生できます。Streamlit Community Cloud は利用状況によりアプリがスリープする場合があります。
