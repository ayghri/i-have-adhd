<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD 친화적인 출력. ADHD 진단은 필요 없어요!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <strong title="한국어" aria-label="한국어">🇰🇷</strong> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a>
</p>


## 설치

🔗 [설치 안내](../install/INSTALL.ko.md)

## 무슨 일을 하나

코딩 어시스턴트가 답을 긴 글 속에 묻어두지 못하게 막는 스킬입니다. **행동 우선**, 단계는 **번호로**, "도움이 되었기를!" 같은 군더더기 없음.


## 무엇이 달라지는가


<table>
<tr>
<td width="50%">

## 사용 전

> 좋은 질문이네요! 한번 생각해볼게요. 인증 흐름에는 미들웨어, 토큰 검증, 쿠키 처리 같은 여러 부분이 있어요. `src/auth.ts`를 살펴보면 `verifyToken` 함수(42~58번째 줄 근처)가 구버전 `jsonwebtoken` API를 쓰는 것 같아요. 한 가지 방법은 패키지를 업데이트하고 그 함수를 다시 작성하는 거예요. 변경 후에는 인증 테스트를 돌려서 문제가 없는지 확인해야 해요. 아, 그리고 하나 더, 전체 의존성 버전도 살펴보시면 좋을 것 같아요. 도움이 되었기를! 더 깊이 파고 싶으시면 알려주세요.

</td>

<td width="50%">

## 사용 후

> `npm install jsonwebtoken@latest` 실행 후 `src/auth.ts:42`를 수정하세요.
>
> 1. `src/auth.ts` 열기
> 2. `verifyToken`(42~58줄)을 아래 스니펫으로 교체
> 3. `npm test -- auth.spec.ts` 실행
>
> 다음 단계: 테스트가 실패하면 첫 번째 실패 줄을 붙여넣어 주세요.

</td>
</tr>
</table>


## 규칙

10가지 규칙. 전문은 [SKILL.md](../../skills/i-have-adhd/SKILL.md)에 있습니다.

1. 다음 행동부터 말하기.
2. 다단계 작업은 번호로.
3. 한 가지 구체적인 다음 단계로 끝내기.
4. 엉뚱한 이야기 자르기.
5. 매 턴마다 현재 상태 다시 알리기.
6. 시간은 분 단위로 정확하게 ("조금" ❌).
7. 진전 사항을 눈에 띄게.
8. 오류는 담백하게.
9. 목록은 최대 5개 항목.
10. 서론, 요약, 마무리 인사 없음.

## 커스터마이즈

저장소를 포크해 `skills/i-have-adhd/SKILL.md`를 수정한 다음, 본인 복사본으로 교체하세요:

```bash
claude plugin uninstall i-have-adhd            # 먼저 업스트림 버전 제거
claude plugin marketplace remove i-have-adhd   # 포크와 업스트림이 같은 이름을 씁니다
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Claude Code를 재시작한 뒤 `/i-have-adhd`를 다시 호출하세요.

## 크레딧

J. Russell Ramsay와 Anthony L. Rostain의 *The Adult ADHD Tool Kit*을 느슨하게 참고했습니다. 사람이 하루를 어떻게 꾸려야 하는가가 아니라 **LLM이 어떻게 응답해야 하는가**에 맞춰 재해석했습니다.

## 라이선스

MIT.

"좋은 질문이네요!" 없는 답변을 한 번이라도 받았다면 Star ⭐ 부탁드립니다.
