# 설치 방법

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### 설치

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 확인

```bash
agy plugin list
```

### 업데이트

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 제거

```bash
agy plugin uninstall i-have-adhd
```

설치된 상태로 비활성화하려면 `agy plugin disable i-have-adhd`를 실행하세요.

### 항상 활성화(선택 사항)

`~/.gemini/GEMINI.md`에 추가하세요:

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### 설치

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

`/i-have-adhd`를 입력하세요.

### 확인

```bash
claude plugin list
```

### 업데이트

```bash
claude plugin marketplace update i-have-adhd
```

### 제거

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

설치된 상태로 비활성화하려면 `claude plugin disable i-have-adhd`를 실행하세요.

### 항상 활성화(선택 사항)

`SessionStart` 훅이 매 세션 시작 시 전체 규칙을 불러오므로 `/i-have-adhd`를 입력할 필요가 없습니다:

```bash
touch ~/.claude/.i-have-adhd-always
```

필요할 때만 켜는 방식으로 돌아가려면:

```bash
rm ~/.claude/.i-have-adhd-always
```

훅은 플래그 파일이 있을 때만 실행되므로 플러그인 설치만으로는 아무것도 바뀌지 않습니다. 설정 디렉터리를 옮겼다면 `$CLAUDE_CONFIG_DIR`를 따릅니다. "stop adhd mode"는 현재 세션에서 계속 비활성화합니다.

</details>


<details>
<summary><strong>Codex</strong></summary>

### 설치

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

`$i-have-adhd`를 명시적으로 입력해 활성화하세요. Codex는 이 스킬을 자동으로 호출하지 않습니다.

### 확인

```bash
codex plugin list
```

### 업데이트

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### 제거

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### 항상 활성화(선택 사항)

`~/.codex/AGENTS.md`에 추가하세요:

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI에는 플러그인 마켓플레이스가 없어 두 가지 기본 방법을 제공합니다. 호출 전까지 꺼져 있는 **사용자 지정 명령**(선택 활성화)과 설치 후 항상 켜지는 **확장 프로그램**입니다. 명령 방식이 이 스킬의 기본 동작과 같으므로 모든 세션에서 규칙을 원하지 않는다면 이 방식을 선택하세요.

### 설치 (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

새 세션을 시작하고 `/i-have-adhd`를 입력하세요. 해당 세션 동안 활성화됩니다.

### 설치 (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

확장 프로그램은 전체 스킬을 가져오는 `GEMINI.md`를 불러오므로 첫 메시지부터 규칙이 적용됩니다. `git`이 설치되어 있어야 합니다.

### 확인

```bash
gemini extensions list          # 확장 프로그램 방식
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

또는 세션에서 `/`를 입력하고 `i-have-adhd`가 목록에 있는지 확인하세요.

### 업데이트

```bash
gemini extensions update i-have-adhd    # 확장 프로그램 방식
# 명령 방식: 위 curl 다시 실행
```

### 제거

```bash
gemini extensions uninstall i-have-adhd    # 확장 프로그램 방식
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot은 Agent Skills를 기본 지원하므로 같은 `SKILL.md`를 변환 없이 읽습니다. 프로젝트의 `.github/skills/`, `.claude/skills/`, `.agents/skills/`와 전역의 `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`를 검색합니다.

### 설치

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # 이 프로젝트
npx skills add ayghri/i-have-adhd -a github-copilot -g     # 모든 프로젝트
```

CLI 없이 설치하려면 스킬 폴더를 Copilot이 검색하는 디렉터리 중 하나에 복사하세요:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### 확인

채팅 입력란에 `/`를 입력하고 `i-have-adhd`가 나타나는지 확인하세요. 또는:

```bash
npx skills list
npx skills ls -g    # 전역 설치한 경우
```

### 업데이트

```bash
npx skills update i-have-adhd
```

또는 `git pull` 후 폴더를 다시 복사하세요.

### 제거

```bash
npx skills remove i-have-adhd
```

또는 설치된 skills 디렉터리에서 `i-have-adhd` 폴더를 삭제하세요.

### 활성화 참고 사항

Copilot은 `disable-model-invocation`을 따릅니다. Claude Code와 마찬가지로 스킬을 호출하기 전에는 아무 규칙도 적용되지 않습니다([#60](https://github.com/ayghri/i-have-adhd/pull/60)에서 테스트).

### 항상 활성화(선택 사항)

아래 블록을 프로젝트의 `.github/copilot-instructions.md`에 추가하세요(Copilot이 모든 채팅에서 읽습니다):

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### 설치

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

`/i-have-adhd`를 입력하세요. The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

먼저 둘러보려면 이 저장소를 스킬 소스("tap")로 추가한 뒤 검색하고 설치하세요:

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### 확인

```bash
hermes skills list
```

### 업데이트

```bash
hermes skills update i-have-adhd
```

### 제거

```bash
hermes skills uninstall i-have-adhd
```

tap도 제거하려면 `hermes skills tap remove ayghri/i-have-adhd`를 실행하세요.

### 항상 활성화(선택 사항)

작업 디렉터리의 `AGENTS.md`(Hermes가 작업 디렉터리별로 불러옴) 또는 모든 세션에 적용할 페르소나의 `SOUL.md`에 추가하세요:

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### 설치

Kimi Code 세션을 시작한 뒤 다음을 수행하세요.

1. `/plugins`를 실행합니다.
2. **Custom**을 선택합니다.
3. `https://github.com/ayghri/i-have-adhd`를 붙여넣고 Enter를 누릅니다.
4. **Trust and install**을 선택합니다.

slash 명령 `/skill:i-have-adhd`로 이 스킬을 명시적으로 호출하세요.

### 업데이트

Kimi Code 세션에서 `/plugins`를 실행하고 **I Have ADHD**에 커서를 맞춘 뒤 `R`을 누르세요.

### 제거

Kimi Code 세션에서 `/plugins`를 실행하고 **I Have ADHD**에 커서를 맞춘 뒤 `D`를 누르세요.

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi는 이 저장소를 네이티브 패키지로 인식합니다. `extensions/`가 세션 지속 모드를 제공하고, `skills/`가 Agent Skills 진입점을 계속 제공합니다.

### 설치

```bash
pi install https://github.com/ayghri/i-have-adhd
```

새 Pi 세션을 시작하세요. 현재 세션에서 ADHD 친화적 출력을 켜고 끕니다:

```text
/i-have-adhd
```

모드가 활성화된 동안 하단에 `● ADHD ON`이 표시됩니다. 명령을 다시 실행하면 꺼지며, 명시적으로 지정할 수도 있습니다:

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

Claude Code 훅과 마찬가지로, 이 확장은 매 요청마다 시스템 프롬프트를 다시 쓰는 대신 대화에 규칙을 한 번만 추가하고, 컴팩션으로 규칙이 사라지면 다시 추가합니다.

기존 Agent Skills 명령도 별칭으로 계속 사용할 수 있습니다:

```text
/skill:i-have-adhd
```

기본적으로 모드가 켜진 상태로 새 Pi 세션을 시작합니다:

```bash
pi --adhd
```

### 확인

```bash
pi list
```

GitHub 패키지가 목록에 있는지 확인한 다음 `/i-have-adhd`를 입력하고 하단에 `● ADHD ON`이 표시되는지 확인하세요.

### 업데이트

```bash
pi update https://github.com/ayghri/i-have-adhd
```

또는 `pi update --extensions`로 버전 고정이 없는 모든 Pi 패키지를 업데이트하세요.

### 제거

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### 항상 활성화(선택 사항)

Pi의 에이전트 설정 디렉터리에 플래그 파일을 만드세요:

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

이 확장은 새로 시작, 재개, 포크, 다시 불러온 모든 세션에서 이 플래그를 확인합니다. 현재 세션에서 저장된 선택은 이 기본값보다 우선하므로, "stop adhd mode"를 실행하면 해당 세션에서는 계속 비활성화됩니다.

필요할 때만 켜는 방식으로 돌아가려면:

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

`PI_CODING_AGENT_DIR`가 설정되어 있다면 `.i-have-adhd-always`를 그 디렉터리에 대신 두세요. 플래그를 변경한 후에는 `/reload`를 실행하거나 새 세션을 시작하세요.

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### 설치

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code는 GitHub 축약 표기를 지원하며 이 저장소를 네이티브 확장으로 설치합니다. 확장은 `skills/` 아래의 스킬을 검색합니다.

`/i-have-adhd`를 입력해 이 스킬을 명시적으로 호출하세요. 확장만 설치해도 스킬을 호출하기 전까지 출력은 바뀌지 않습니다.

### 확인

```bash
qwen extensions list
```

그런 다음 새 Qwen Code 세션을 시작하고 다음을 실행하세요.

```text
/skills
```

목록에 `i-have-adhd`가 표시되는지 확인하세요.

### 업데이트

```bash
qwen extensions update i-have-adhd
```

### 제거

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed의 Agent는 Agent Skills를 기본 지원하므로 같은 `SKILL.md`를 변환 없이 읽습니다. (기존 "Rules"는 Skills와 `AGENTS.md` 지침으로 대체되었습니다.)

### 설치

Agent Panel에서 Skills 관리자를 열고 **Create skill from URL**(명령 팔레트에서는 `agent: create skill from url`)을 선택한 뒤 다음을 붙여넣으세요:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

모든 프로젝트에서 사용하려면 **User** 범위에, 한 프로젝트에서만 사용하려면 **Project** 범위에 저장하세요. 그런 다음 Agent Panel에서 `/i-have-adhd`를 입력하세요.

파일 시스템 방식을 선호한다면 저장소를 클론하고 스킬 폴더를 사용자 skills 디렉터리에 넣으세요:

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### 확인

Agent Panel에서 Skills 관리자를 열어 `i-have-adhd`가 목록에 있는지 확인하세요. 또는 `/`를 입력해 나타나는지 확인하세요.

### 업데이트

같은 URL에서 다시 가져오거나(덮어쓰기) `git pull` 후 폴더를 다시 복사하세요.

### 제거

Skills 관리자에서 `i-have-adhd`를 제거하거나 `~/.config/zed/skills/i-have-adhd`를 삭제하세요.

### 항상 활성화(선택 사항)

개인 `~/.config/zed/AGENTS.md`에 추가하세요:

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp 및 기타 agent-skills 실행 환경</strong></summary>

Agent Skills를 읽는 모든 실행 환경에서 작동합니다. `-a <agent>`를 사용하는 에이전트로 바꾸세요.

### 설치

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # 모든 프로젝트
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

새 에이전트 채팅에서 `/i-have-adhd`를 입력하세요.

CLI 없이 설치하려면 에이전트가 검색하는 경로에 스킬 폴더를 복사하세요:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. OpenCode는 .agents/skills, 다른 에이전트는 자체 경로 사용
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### 확인

```bash
npx skills list
npx skills ls -g    # 전역 설치한 경우
```

### 업데이트

```bash
npx skills update i-have-adhd
npx skills update -g    # 전역 설치한 경우
```

### 제거

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # 전역 설치한 경우
```

### 항상 활성화(선택 사항)

에이전트의 영구 규칙 파일에 다음을 붙여넣으세요. Cursor: **Settings → Rules → User Rules** 또는 `.cursor/rules/` 아래 `alwaysApply: true`인 프로젝트 규칙. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## 출력 스타일

읽는 사람은 ADHD가 있습니다. 모든 답변을 바로 실행할 수 있도록 구성하세요:

1. 답이나 다음 행동부터 제시하세요. 명령어, 경로 또는 코드 조각을 먼저 보여 주세요.
2. 여러 단계의 작업에는 번호를 붙이고, 단계마다 범위가 명확한 행동 하나만 두세요.
3. 2분 안에 할 수 있는 다음 행동 하나로 끝내세요.
4. 새 문제를 꺼내기 전에 현재 문제를 마무리하세요.
5. 매 턴마다 진행 상황을 다시 알려 주세요("5단계 중 3단계 완료").
6. 시간은 구체적인 단위로 예상하고 "조금"이라고 하지 마세요.
7. 변경 후에는 이제 무엇이 작동하는지 보여 주세요.
8. 오류는 위치, 원인, 해결 방법을 담담하게 알려 주세요.
9. 목록은 최대 5개 항목으로 제한하세요.
10. 서론, 요약, 마무리 인사를 넣지 마세요.

예외: 설명을 요청받으면 충분히 설명하세요. 파괴적인 작업 전에는 확인하세요. 세 번의 수정이 실패하면 멈추고 의심되는 가정을 밝히세요. 요청이 모호하면 짧은 질문 하나를 하세요.
```
</details>


## 활성화 방식

1. **설치했지만 호출하지 않은 상태.** Claude Code, Qwen Code, Codex에서는 명시적으로 호출하기 전까지 아무 일도 일어나지 않습니다. Claude Code와 Qwen Code는 `SKILL.md`의 `disable-model-invocation: true`를 따르고, Codex는 `agents/openai.yaml`의 `policy.allow_implicit_invocation: false`를 따릅니다. 다른 실행 환경은 시작 시 각 스킬 설명을 불러와 스스로 활성화할 수 있습니다.
2. **명시적으로 호출합니다.** Claude Code와 Qwen Code에서는 `/i-have-adhd`를, Codex에서는 `$i-have-adhd`를 입력합니다. 해당 세션에서 규칙이 활성화됩니다. "stop adhd mode" 또는 "normal mode"로 끌 수 있습니다.
3. **`~/.claude/.i-have-adhd-always`를 만듭니다**(Claude Code). `SessionStart` 훅이 매 세션의 첫 메시지부터 전체 규칙을 불러옵니다.
4. **위의 항상 활성화 코드 조각을 추가합니다**(기타 실행 환경). 핵심 규칙이 에이전트의 영구 컨텍스트에 유지됩니다.

Claude Code, Qwen Code, Codex에는 중간 상태가 없습니다. 켜지 않았다면 꺼져 있습니다.

## 문제 해결

**자동 완성에 `/i-have-adhd`가 없습니다.** 에이전트를 다시 시작하세요. 플러그인 인덱스는 시작 시 읽힙니다.

**항상 활성화 플래그가 작동하지 않습니다.** 플러그인을 업데이트하고(`claude plugin marketplace update i-have-adhd`) 다시 시작하세요. 훅은 시작 시 읽히며 플래그에는 `hooks/hooks.json`이 포함된 플러그인 버전이 필요합니다.

**`claude plugin marketplace add`가 실패합니다.** `owner/repo` 형식을 사용하세요. 로컬 경로는 `.claude-plugin/`이 아니라 저장소 루트를 가리켜야 합니다.

**설치했지만 답변에 여전히 서론이 있습니다.** 새 세션을 여세요. 계속 어긋난다면 `skills/i-have-adhd/SKILL.md`의 표현을 더 엄격하게 바꾸세요.

**다른 규칙을 원합니다.** 저장소를 포크하고 `skills/i-have-adhd/SKILL.md`를 수정한 뒤 자신의 복사본으로 교체하세요:

```bash
claude plugin uninstall i-have-adhd            # 먼저 업스트림 복사본 제거:
claude plugin marketplace remove i-have-adhd   # 포크와 업스트림은 같은 이름 사용
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

다시 시작한 뒤 `/i-have-adhd`를 다시 호출하세요.

**`npx skills add` 후 스킬이 보이지 않습니다.** 새 에이전트 채팅을 시작하세요. 스킬은 세션 시작 시 인덱싱됩니다. 폴더가 에이전트 검색 경로(Cursor는 `~/.cursor/skills/`, OpenCode는 `.agents/skills/`)에 있고 frontmatter의 `name`이 폴더 이름과 같은지 확인하세요.
