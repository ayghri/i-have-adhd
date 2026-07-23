<p align="center">
  <img src="./logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD に配慮した出力。ADHD の診断は不要です！</strong>
</p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/merx666/i-have-adhd-antigravity?style=flat" alt="ライセンス"></a>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <strong>日本語</strong>
</p>


## インストール

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add merx666/i-have-adhd-antigravity
claude plugin install i-have-adhd@i-have-adhd
```

続いて `/i-have-adhd` と入力します。ローカルへのクローンは不要です。Claude Code がリポジトリを取得し、最新の状態に保ちます。

すべてのセッションで使いたい場合は、`touch ~/.claude/.i-have-adhd-always` を実行してください（[INSTALL.md](./INSTALL.md) を参照）。

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add merx666/i-have-adhd-antigravity --ref main
codex plugin add i-have-adhd@i-have-adhd
```

続いて `$i-have-adhd` と入力すると、この出力スタイルが明示的に適用されます。Codex がこのスキルに適したタスクだと判断した場合は、暗黙的に呼び出されることもあります。

</details>

その他のコーディングエージェント向けのインストール手順は [INSTALL.md](./INSTALL.md) にあります。

## 機能

コーディングアシスタントが答えを長い文章に埋もれさせないようにするスキルです。行動を先に。手順には番号を。「お役に立てれば幸いです！」は不要です。


## 変わること


<table>
<tr>
<td width="50%">

## 適用前

> 良い質問ですね！考えてみましょう。認証フローには、ミドルウェア、トークン検証、Cookie の処理といういくつかの要素があります。`src/auth.ts` を見ると、`verifyToken` 関数（42～58 行目付近）は古い `jsonwebtoken` API を使っているようです。一つの方法は、パッケージを更新してその関数を書き直すことです。変更後は、認証テストを実行して問題が起きていないことを確認するとよいでしょう。ついでに、依存関係のバージョンも全体的に確認したほうがよいかもしれません。お役に立てれば幸いです！さらに詳しく調べたい場合はお知らせください。

</td>

<td width="50%">

## 適用後

> `npm install jsonwebtoken@latest` を実行してから、`src/auth.ts:42` を編集してください。
>
> 1. `src/auth.ts` を開く
> 2. `verifyToken`（42～58 行目）を以下のスニペットに置き換える
> 3. `npm test -- auth.spec.ts` を実行する
>
> 次の手順：テストが失敗した場合は、最初のエラー行を貼り付けてください。

</td>
</tr>
</table>


## ルール

ルールは 10 個です。全文は [SKILL.md](./skills/i-have-adhd/SKILL.md) にあります。

1. 次に取る行動から始める。
2. 複数手順のタスクには番号を付ける。
3. 具体的な次の一手を一つ示して終える。
4. 脱線を抑える。
5. ターンごとに現在の状態を言い直す。
6. 具体的な所要時間を示す（「少し」ではなく分単位）。
7. 成果を目に見える形で示す。
8. エラーを淡々と伝える。
9. リストは 5 項目までにする。
10. 前置き、要約、締めの言葉を入れない。

## カスタマイズ

リポジトリを Fork し、`skills/i-have-adhd/SKILL.md` を編集してから、自分のコピーに切り替えます。

```bash
claude plugin uninstall i-have-adhd            # まず上流のコピーを削除：
claude plugin marketplace remove i-have-adhd   # fork と上流では同じ名前が使われる
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Claude Code を再起動し、`/i-have-adhd` をもう一度呼び出してください。

## クレジット

J. Russell Ramsay と Anthony L. Rostain による *The Adult ADHD Tool Kit* を大まかに参考にしています。人間が一日をどう整理すべきかではなく、LLM がどう応答すべきかに合わせて改変したものです。

## ライセンス

MIT。

「良い質問ですね！」を一度スクロールして読み飛ばさずに済んだなら、Star ⭐ をお願いします。
