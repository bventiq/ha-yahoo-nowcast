# Yahoo! Weather Nowcast for Home Assistant

Yahoo! JAPAN Weather APIの降水ナウキャストを使用したホームアシスタント統合です。

---

## 🇯🇵 日本語版

### 概要

Yahoo! JAPAN Weather APIを使用したリアルタイム降水予測ホームアシスタント統合です。エリア内の降水を監視・予測するためのセンサーおよびバイナリセンサーエンティティを提供します。

### Yahoo! JAPAN Weather APIについて

このインテグレーションはYahoo! JAPANの気象情報APIを利用しています。

- **提供情報**: リアルタイム降水予測（ナウキャスト）、気温、湿度
- **更新間隔**: 5分ごと
- **対応地域**: 日本国内
- **API仕様**: RESTful API（JSON形式）
- **制限事項**: リクエストレート制限あり

**Client ID取得方法:****
1. [Yahoo! JAPAN デベロッパーネットワーク](https://developer.yahoo.co.jp/)にアクセス
2. Yahoo! JAPANのアカウントでログイン（またはアカウント作成）
3. 「アプリケーション管理」から新しいアプリケーションを登録
4. 「気象情報API」を選択・申し込み
5. Client IDを取得

**重要:** Yahoo! JAPANの利用規約に従ってください。このインテグレーションの使用は、Yahoo! JAPANの利用規約に同意したものとみなされます。

### 機能

- **降水量予測センサー**: 今後30分間の予測降水量を表示
- **雨アラートバイナリセンサー**: 降水が予想される時の通知
- **気温・湿度センサー**: 追加の気象情報
- **カスタマイズ可能なパラメータ**: 検知閾値と予測期間を調整
- **リアルタイム更新**: デフォルトで5分ごとに更新

### インストール方法

#### 方法1: HACS (Home Assistant Community Store)
1. Home AssistantでHACSを開く
2. 「Integrations」をクリック
3. メニューボタンをクリックして「Custom repositories」を選択
4. リポジトリURLを追加
5. 統合をインストール
6. Home Assistantを再起動

#### 方法2: 手動インストール
1. このリポジトリの`custom_components/yahoo_nowcast_jp`フォルダを、Home Assistantの`/config/custom_components/yahoo_nowcast_jp`にコピー
2. Home Assistantを再起動
3. 設定 → デバイスとサービス → 統合から追加

### 設定方法

#### 設定ステップ
1. 設定 → デバイスとサービス → 統合に移動
2. 「統合を作成」をクリック
3. 「Yahoo! Weather Nowcast」を検索
4. Yahoo! JAPAN Client IDを入力
5. 緯度、経度、その他のパラメータを設定

#### 設定パラメータ
- **Client ID**: Yahoo! JAPAN Weather APIのClient ID（必須）
- **緯度**: 観測位置の緯度（必須）
- **経度**: 観測位置の経度（必須）
- **検知閾値**: アラートをトリガーする最小降水量（mm/h、デフォルト：0.2）
- **予測時間**: 予測期間（分、デフォルト：30）

### エンティティ

#### センサー
- `sensor.precipitation_forecast`: 現在の降水予測（mm/h）
- `sensor.temperature`: 現在の気温（°C）
- `sensor.humidity`: 現在の湿度（%）

#### バイナリセンサー
- `binary_sensor.rain_soon`: 予測時間内に降水が予想される場合はTrue

### トラブルシューティング

#### APIに接続できない
- Client IDが正しいか確認してください
- インターネット接続を確認してください
- APIエンドポイントにアクセスできることを確認してください

#### 認証が無効
- Client IDが有効かつアクティブであることを確認してください
- Yahoo! JAPAN APIドキュメントでキー要件を確認してください

#### データが表示されない
- 緯度と経度が正しいか確認してください
- Home Assistantのログで詳細なエラーメッセージを確認してください
- 統合が適切に設定されていることを確認してください

### サポート

問題、質問、提案については、[GitHubリポジトリ](https://github.com/yourusername/jma_precipitation_nowcast)をご覧ください。

---

## 🇬🇧 English Version

### Overview

This Home Assistant integration provides real-time precipitation forecasts using Yahoo! JAPAN Weather API. It offers both sensor and binary sensor entities to monitor and predict rainfall in your area.

### About Yahoo! JAPAN Weather API

This integration utilizes Yahoo! JAPAN's weather information API.

- **Information Provided**: Real-time precipitation forecasts (nowcast), temperature, humidity
- **Update Interval**: Every 5 minutes
- **Coverage Area**: Japan only
- **API Specification**: RESTful API (JSON format)
- **Limitations**: Request rate limiting applies

**How to Get an API Key:**
1. Visit [Yahoo! JAPAN Developer Network](https://developer.yahoo.co.jp/)
2. Log in with your Yahoo! JAPAN account (or create one)
3. Go to "Application Management" and register a new application
4. Select and apply for the "Weather Information API"
5. Obtain your API key

**Important:** Please comply with Yahoo! JAPAN's terms of service. Use of this integration is deemed acceptance of Yahoo! JAPAN's terms of service.

### Features

- **Precipitation Forecast Sensor**: Displays predicted precipitation levels for the next 30 minutes
- **Rain Alert Binary Sensor**: Binary alert when rainfall is expected
- **Temperature & Humidity Sensors**: Additional weather information
- **Configurable Parameters**: Adjust detection thresholds and forecast duration
- **Real-time Updates**: Updates every 5 minutes by default

### Installation

#### Method 1: HACS (Home Assistant Community Store)
1. Open HACS in Home Assistant
2. Click "Integrations"
3. Click the menu button and select "Custom repositories"
4. Add the repository URL
5. Install the integration
6. Restart Home Assistant

#### Method 2: Manual Installation
1. Copy the `custom_components/yahoo_nowcast_jp` folder from this repository to `/config/custom_components/yahoo_nowcast_jp` on your Home Assistant
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

### Configuration

#### Setup via UI
1. Go to Settings → Devices & Services → Integrations
2. Click "Create Integration"
3. Search for "Yahoo! Weather Nowcast"
4. Enter your Yahoo! JAPAN API key
5. Configure latitude, longitude, and other parameters

#### Configuration Parameters
- **API Key**: Yahoo! JAPAN Weather API key (required)
- **Latitude**: Location latitude (required)
- **Longitude**: Location longitude (required)
- **Detection Threshold**: Minimum precipitation level to trigger alerts (mm/h, default: 0.2)
- **Forecast Minutes**: Forecast duration in minutes (default: 30)

### Entities

#### Sensors
- `sensor.precipitation_forecast`: Current precipitation forecast (mm/h)
- `sensor.temperature`: Current temperature (°C)
- `sensor.humidity`: Current humidity (%)

#### Binary Sensors
- `binary_sensor.rain_soon`: True when rain is expected within the forecast window

### Troubleshooting

#### Cannot connect to API
- Verify your API key is correct
- Check your internet connection
- Confirm the API endpoint is accessible

#### Invalid authentication
- Ensure the API key is valid and active
- Check Yahoo! JAPAN API documentation for key requirements

#### No data displayed
- Verify latitude and longitude are correct
- Check Home Assistant logs for detailed error messages
- Ensure the integration is properly configured

### Support

For issues, questions, or suggestions, please visit the [GitHub repository](https://github.com/yourusername/jma_precipitation_nowcast).

---

## License

This integration is provided as-is for use with Home Assistant.

## Disclaimer

This integration is not affiliated with the Japan Meteorological Agency (JMA) or Yahoo! JAPAN. Use of the Yahoo! JAPAN Weather API is subject to their terms of service.
