# 宇都宮ジャパンカップクリテリウム 2026 — コース概略3Dモデル

## ファイル
- `utsunomiya_japan_cup_2026.blend`：編集可能なBlenderシーン
- `course_overview.png`：コース全景
- `banba_detail.png`：バンバひろば付近
- `build_course.py`：再生成用スクリプト（Blender 4.3）
- `validation.json`：走行ラインの長さなどの検証結果

## 基準資料
公式2026年コース紹介：https://www.japancup.gr.jp/y2026/criterium/
公式コース図：https://www.japancup.gr.jp/wp/wp-content/uploads/2026/09/2026-criterium-course-map.jpeg
確認日：2026-09-29

公式資料で確認した事項：大通りの往復周回、東武馬車道通り入口と上河原交差点での折り返し、バンバひろばでのスタート／フィニッシュ、1周2.25km。北側車線が西向き、南側車線が東向き。

## 再現範囲と仮定
これは公式案内図を基にした概略・展示用モデルで、測量やGISに基づく都市モデルではありません。道路は直線化し、道路幅27m・走行ライン折り返し半径8mを仮定。周回線の長さを約2250mに合わせています。道路の実際の曲がり、勾配、標高は再現していません。建物の位置・高さ・形状、神社、樹木、イベント設備は説明用の推定表現です。実在施設の正確な外観や当日の設備配置を示すものではありません。

## 操作
単位はメートル。Xが東、Yが北、Zが上。8つのコレクションで道路、街並み、ランドマーク、設備、走行ライン、植栽、注釈、カメラを整理しています。
カメラは全景、バンバひろば、真上の3種類。走行ラインは編集可能な閉じたカーブです。注釈を非表示にすると街並みのみを表示できます。

再生成：
```sh
'/Applications/Blender 4.3.app/Contents/MacOS/Blender' --background --python build_course.py
```

## 自転車目線の3秒動画
- `utsunomiya_cyclist_pov_3s.mp4`：1280×720、24fps、72フレーム、無音のH.264 MP4。
- `utsunomiya_cyclist_pov_3s.blend`：カメラのアニメーション付きシーン。
- `animate_ride.py`：既存モデルから動画を再生成するスクリプト。
- `cyclist_pov_preview.png`：スタート位置の目線確認画像。

バンバひろばのスタート線から北側車線を西へ進み、両端を折り返して同じスタート／フィニッシュ線まで1周します。カメラ高は1.65m、広角20mm。2.25kmの1周を3秒に圧縮した早送り表現で、実際の自転車の走行速度ではありません。全景用の赤いコース線・方向矢印を動画では非表示にしています。

## レース想定速度の動画
`utsunomiya_race_pov_50kmh.mp4` は1周162秒（2分42秒）、1280×720、24fps、無音。平均約50km/h、直線の巡航約56.85km/h、折り返し約18km/hで、カーブ前後65mで滑らかに減速・加速します。速度は演出用に設計したもので、実際の選手の走行記録ではありません。目線の高さは1.65mです。

`utsunomiya_race_pov_50kmh.blend` にカメラアニメーションを保存し、`animate_race.py` で再生成できます。長尺動画はWorkbenchレンダラーのマテリアル色・陰影で描画しています。

## ハイライト編集
- `course_6_highlights.mp4`：最新版。30秒・4,225,777バイト。スタート、大通り、西側ヘアピン、ヘアピン間の直線、東側ヘアピン、ゴール前の6場面。
- `course_5_highlights.mp4`：初版。25秒・3,534,073バイト。5場面。
- `course_6_highlights_edit.blend` / `edit_highlights_6.py`：最新版の編集シーンと再生成スクリプト。
- `course_5_highlights_edit.blend` / `edit_highlights.py`：初版の編集シーンと再生成スクリプト。

どちらも960×540・24fps・無音のMP4で、5,000,000バイト以内。`highlights_6_edit.json` と `highlights_edit.json` に切り出し位置とサイズを記録しています。再編集には同じフォルダの `utsunomiya_race_pov_50kmh.mp4` を使用します。
