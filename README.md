# JMA Precipitation Nowcast

日本気象協会（JMA）のナウキャストを使用した降水予測ホームアシスタント統合です。

---

## 🇯🇵 日本語版

### 概要

Yahoo! JAPAN Weather APIを使用したリアルタイム降水予測ホームアシスタント統合です。エリア内の降水を監視・予測するためのセンサーおよびバイナリセンサーエンティティを提供します。

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
1. `jma_precipitation_nowcast`フォルダをHome Assistantの`custom_components`ディレクトリにコピー
2. Home Assistantを再起動
3. 設定 → デバイスとサービス → 統合から追加

### 設定方法

#### UIを使用した設定
1. 設定 → デバイスとサービス → 統合に移動
2. 「統合を作成」をクリック
3. 「JMA Precipitation Nowcast」を検索
4. Yahoo! JAPAN APIキーを入力
5. 緯度、経度、その他のパラメータを設定

#### 設定パラメータ
- **APIキー**: Yahoo! JAPAN Weather APIキー（必須）
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
- APIキーが正しいか確認してください
- インターネット接続を確認してください
- APIエンドポイントにアクセスできることを確認してください

#### 認証が無効
- APIキーが有効かつアクティブであることを確認してください
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
1. Copy the `jma_precipitation_nowcast` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

### Configuration

#### Setup via UI
1. Go to Settings → Devices & Services → Integrations
2. Click "Create Integration"
3. Search for "JMA Precipitation Nowcast"
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
