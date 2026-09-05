<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHDに配慮した簡潔な出力。（診断済みかは関係なく、誰でも気軽に使えます！）</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="ライセンス"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <strong title="日本語" aria-label="日本語">🇯🇵</strong> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a>
</p>

## インストール

CLIのプロンプトに以下をコピー＆ペーストしてください：

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

または、🔗 [インストール手順を確認する](../install/INSTALL.ja.md)。

## 機能

コーディングアシスタントの回答を長文で埋めさせないようにするスキル。最優先は行動で、手順を箇条書きで整理。  「お役に立てれば幸いです！」などの不要な挨拶や定型文をカットします。

## 変化の例

<table>
<tr>
<td width="50%">

## 適用前

> 良い質問ですね！考えてみましょう。認証フローには、ミドルウェア、トークン検証、Cookieの処理といういくつかの要素があります。`src/auth.ts` を見ると、`verifyToken` 関数（42〜58行目付近）は古い `jsonwebtoken` API を使っているようです。一つの方法としては、パッケージを更新してその関数を書き直すことです。変更後は、認証テストを実行して問題が起きていないことを確認するとよいでしょう。ついでに、依存関係のバージョンも全体的に確認したほうがよいかもしれません。お役に立てれば幸いです！さらに詳しく調べたい場合はお知らせください。

</td>

<td width="50%">

## 適用後

> `npm install jsonwebtoken@latest` を実行後、`src/auth.ts:42` を編集する。
>
> 1. `src/auth.ts` を開く
> 2. `verifyToken`（42〜58行目）を以下のスニペットに置き換える
> 3. `npm test -- auth.spec.ts` を実行する
>
> 次の行動：テストが失敗した場合は、最初のエラー行を貼り付ける。

</td>
</tr>
</table>

## 10のルール

ルールは10個。全文は [SKILL.md](../../skills/i-have-adhd/SKILL.md) を参照してください。

1. 次に取る行動から始める。
2. 複数ステップの作業には番号を付ける。
3. 2分以内にできる具体的な次の一手で終える。
4. 脱線を防ぐ。
5. ターンごとに現在の進捗・状態を明記する。
6. 所要時間は「少し」ではなく分単位で具体的に示す。
7. 変更後に何が動くようになったかを明示する。
8. エラーは場所・原因・対処法だけを淡々と伝える。
9. リストは最大5項目までに抑える。
10. 前置き・要約・締めの挨拶は入れない。

## カスタマイズ

リポジトリをForkし、`skills/i-have-adhd/SKILL.md` を編集してから自分のコピーに差し替えます。

```bash
claude plugin uninstall i-have-adhd            # 先に本家のコピーを削除
claude plugin marketplace remove i-have-adhd   # Fork版と本家で名前が重複するため
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Claude Code を再起動し、`/i-have-adhd` をもう一度呼び出してください。

## クレジット

J. Russell Ramsay と Anthony L. Rostain による著書『*The Adult ADHD Tool Kit*』に着想を得ています。人間の一日のスケジュール管理ではなく、LLMがどう返答すべきかに合わせて最適化しています。

## ライセンス

MIT

もし1回でも「良い質問ですね！」を読み飛ばすスクロールが減ったなら、Star⭐️をお願いします。
