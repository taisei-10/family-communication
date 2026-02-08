# Family Communication App

家族向けコミュニケーションアプリ。帰宅時間、食事の有無、車の予約などを家族で共有。

## プロジェクト構造

```
family-communication/
├── backend/          # FastAPI (Python)
│   └── app/
│       ├── models/         # データベースモデル (SQLAlchemy)
│       │   ├── users.py    # ユーザーモデル
│       │   ├── family.py   # 家族グループモデル
│       │   └── schedule.py # スケジュールモデル (帰宅/食事/車/イベント)
│       ├── schemas/        # API入出力の型定義 (Pydantic)
│       │   ├── users.py
│       │   ├── family.py
│       │   └── schedule.py
│       ├── routers/        # APIエンドポイント
│       │   ├── auth.py     # 認証 (登録/ログイン)
│       │   ├── users.py    # ユーザー管理
│       │   ├── families.py # 家族グループ管理
│       │   └── schedules.py # スケジュール管理
│       ├── utils/          # ユーティリティ
│       │   ├── auth.py     # JWT認証
│       │   └── security.py # パスワードハッシュ化
│       ├── database.py     # DB接続設定
│       └── main.py         # エントリーポイント
└── frontend/         # React + TypeScript + Vite
    └── src/
        ├── types/          # TypeScript型定義
        │   └── index.ts
        ├── services/       # API通信
        │   ├── api.ts      # axios設定
        │   ├── auth.ts     # 認証API
        │   ├── family.ts   # 家族API
        │   └── schedule.ts # スケジュールAPI
        ├── pages/          # ページコンポーネント
        │   └── Login.tsx
        ├── components/     # 再利用可能なコンポーネント
        └── App.tsx         # ルーティング設定

## 主要機能

- **認証**: JWT認証、ユーザー登録/ログイン
- **家族グループ**: 家族の作成/参加/離脱
- **スケジュール**: 統合型スケジュール管理
  - `return`: 帰宅予定
  - `meal`: 食事の有無 (breakfast/lunch/dinner)
  - `car`: 車の予約 (car_name, start_time, end_time)
  - `event`: その他イベント

## データベース

- SQLite (`family_communication.db`)
- SQLAlchemy ORM使用
- テーブル: users, families, schedules

## 実行方法

**バックエンド:**
```bash
cd backend
uvicorn app.main:app --reload
```

**フロントエンド:**
```bash
cd frontend
npm run dev
```
