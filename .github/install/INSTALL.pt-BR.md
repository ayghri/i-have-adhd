# Como instalar

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### Instalar

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Verificar

```bash
agy plugin list
```

### Atualizar

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Desinstalar

```bash
agy plugin uninstall i-have-adhd
```

Ou mantenha instalado e desative: `agy plugin disable i-have-adhd`.

### Sempre ativo (opcional)

Adicione ao `~/.gemini/GEMINI.md`:

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### Instalar

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Digite `/i-have-adhd`.

### Verificar

```bash
claude plugin list
```

### Atualizar

```bash
claude plugin marketplace update i-have-adhd
```

### Desinstalar

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

Ou mantenha instalado e desative: `claude plugin disable i-have-adhd`.

### Sempre ativo (opcional)

Um hook `SessionStart` carrega todas as regras no início de cada sessão; não é preciso usar `/i-have-adhd`:

```bash
touch ~/.claude/.i-have-adhd-always
```

Para voltar ao modo sob demanda:

```bash
rm ~/.claude/.i-have-adhd-always
```

O hook só é executado quando o arquivo de sinalização existe, portanto instalar o plugin não muda nada por si só. Ele respeita `$CLAUDE_CONFIG_DIR` caso você tenha movido o diretório de configuração. "stop adhd mode" ainda o desativa na sessão atual.

</details>


<details>
<summary><strong>Codex</strong></summary>

### Instalar

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Ative a skill explicitamente digitando `$i-have-adhd`. O Codex não a invoca automaticamente.

### Verificar

```bash
codex plugin list
```

### Atualizar

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Desinstalar

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Sempre ativo (opcional)

Adicione ao `~/.codex/AGENTS.md`:

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

O Gemini CLI não tem marketplace de plugins, então há duas opções nativas: um **comando personalizado** (opt-in, desativado até ser invocado) ou uma **extensão** (sempre ativa após a instalação). O comando corresponde ao comportamento padrão desta skill; escolha-o, a menos que queira as regras em todas as sessões.

### Instalar (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

Inicie uma nova sessão e digite `/i-have-adhd`. A skill permanecerá ativa durante essa sessão.

### Instalar (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

A extensão carrega `GEMINI.md`, que importa a skill completa; assim, as regras valem desde a primeira mensagem. O `git` precisa estar instalado.

### Verificar

```bash
gemini extensions list          # via extensão
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

Ou digite `/` em uma sessão e confirme que `i-have-adhd` aparece na lista.

### Atualizar

```bash
gemini extensions update i-have-adhd    # via extensão
# via comando: execute novamente o curl acima
```

### Desinstalar

```bash
gemini extensions uninstall i-have-adhd    # via extensão
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

O Copilot lê Agent Skills nativamente: usa o mesmo `SKILL.md`, sem conversão. No projeto, ele verifica `.github/skills/`, `.claude/skills/` e `.agents/skills/`; globalmente, `~/.copilot/skills/`, `~/.claude/skills/` e `~/.agents/skills/`.

### Instalar

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # este projeto
npx skills add ayghri/i-have-adhd -a github-copilot -g     # todos os projetos
```

Sem a CLI, copie a pasta da skill para qualquer diretório verificado pelo Copilot:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### Verificar

Digite `/` no campo de chat e confirme que `i-have-adhd` aparece. Ou:

```bash
npx skills list
npx skills ls -g    # se instalado globalmente
```

### Atualizar

```bash
npx skills update i-have-adhd
```

Ou copie a pasta novamente após `git pull`.

### Desinstalar

```bash
npx skills remove i-have-adhd
```

Ou exclua a pasta `i-have-adhd` do diretório de skills onde ela foi instalada.

### Observação sobre ativação

O Copilot respeita `disable-model-invocation`: nada é aplicado até você invocar a skill, como no Claude Code (testado no [#60](https://github.com/ayghri/i-have-adhd/pull/60)).

### Sempre ativo (opcional)

Adicione o bloco abaixo ao `.github/copilot-instructions.md` do projeto (o Copilot o lê em todo chat):

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### Instalar

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

Digite `/i-have-adhd`. The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

Prefere explorar primeiro? Adicione este repositório como fonte de skills (um "tap"), depois pesquise e instale:

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### Verificar

```bash
hermes skills list
```

### Atualizar

```bash
hermes skills update i-have-adhd
```

### Desinstalar

```bash
hermes skills uninstall i-have-adhd
```

Ou remova também o tap: `hermes skills tap remove ayghri/i-have-adhd`.

### Sempre ativo (opcional)

Adicione ao `AGENTS.md` do diretório de trabalho (o Hermes o carrega por diretório) ou ao `SOUL.md` da sua persona para todas as sessões:

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### Instalar

Inicie uma sessão do Kimi Code e:

1. Execute `/plugins`.
2. Selecione **Custom**.
3. Cole `https://github.com/ayghri/i-have-adhd` e pressione Enter.
4. Selecione **Trust and install**.

Use o comando slash `/skill:i-have-adhd` para invocar a skill explicitamente.

### Atualizar

Em uma sessão do Kimi Code, execute `/plugins`, posicione o cursor em **I Have ADHD** e pressione `R`.

### Desinstalar

Em uma sessão do Kimi Code, execute `/plugins`, posicione o cursor em **I Have ADHD** e pressione `D`.

</details>


<details>
<summary><strong>Pi</strong></summary>

O Pi identifica este repositório como um pacote nativo: `extensions/` fornece o modo persistente de sessão e `skills/` mantém o ponto de entrada do Agent Skills disponível.

### Instalar

```bash
pi install https://github.com/ayghri/i-have-adhd
```

Inicie uma nova sessão do Pi. Ative ou desative a saída amigável para TDAH na sessão atual:

```text
/i-have-adhd
```

O rodapé mostra `● ADHD ON` enquanto o modo está ativo. Execute o comando novamente para desativar, ou seja explícito:

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

Assim como o hook do Claude Code, a extensão adiciona o conjunto de regras à conversa uma única vez, em vez de reescrever o prompt do sistema a cada solicitação, e o adiciona novamente depois que a compactação o descarta.

O comando Agent Skills existente continua disponível como alias:

```text
/skill:i-have-adhd
```

Inicie uma nova sessão do Pi com o modo ativado por padrão:

```bash
pi --adhd
```

### Verificar

```bash
pi list
```

Confirme que o pacote do GitHub aparece na lista, digite `/i-have-adhd` e verifique se `● ADHD ON` aparece no rodapé.

### Atualizar

```bash
pi update https://github.com/ayghri/i-have-adhd
```

Ou atualize todos os pacotes Pi sem versão fixada com `pi update --extensions`.

### Desinstalar

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### Sempre ativo (opcional)

Crie um arquivo de sinalização no diretório de configuração do agente do Pi:

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

A extensão verifica esse arquivo em toda sessão nova, retomada, bifurcada ou recarregada. Uma escolha salva para a sessão atual tem prioridade sobre esse padrão, então "stop adhd mode" mantém essa sessão desativada.

Para voltar ao modo sob demanda:

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

Se `PI_CODING_AGENT_DIR` estiver definida, coloque `.i-have-adhd-always` nesse diretório. Execute `/reload` ou inicie uma nova sessão após alterar o arquivo de sinalização.

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### Instalar

```bash
qwen extensions install ayghri/i-have-adhd
```

O Qwen Code aceita a forma abreviada do GitHub e instala o repositório como extensão nativa. A extensão encontra a skill em `skills/`.

Digite `/i-have-adhd` para invocar a skill explicitamente. Instalar a extensão não altera a saída até que a skill seja invocada.

### Verificar

```bash
qwen extensions list
```

Depois, inicie uma nova sessão do Qwen Code e execute:

```text
/skills
```

Confirme que `i-have-adhd` aparece na lista.

### Atualizar

```bash
qwen extensions update i-have-adhd
```

### Desinstalar

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

O Agent do Zed lê Agent Skills nativamente: usa o mesmo `SKILL.md`, sem conversão. (As antigas "Rules" do Zed foram substituídas por Skills e instruções em `AGENTS.md`.)

### Instalar

No Agent Panel, abra o gerenciador de Skills, escolha **Create skill from URL** (também disponível na paleta como `agent: create skill from url`) e cole:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

Salve no escopo **User** para todos os projetos ou **Project** para apenas um. Depois, digite `/i-have-adhd` no Agent Panel.

Prefere o sistema de arquivos? Clone o repositório e coloque a pasta da skill no diretório de skills do usuário:

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### Verificar

Abra o gerenciador de Skills no Agent Panel e confirme que `i-have-adhd` aparece. Ou digite `/` e confira.

### Atualizar

Importe novamente pela mesma URL (sobrescreve) ou copie a pasta de novo após `git pull`.

### Desinstalar

Remova `i-have-adhd` do gerenciador de Skills ou exclua `~/.config/zed/skills/i-have-adhd`.

### Sempre ativo (opcional)

Adicione ao seu `~/.config/zed/AGENTS.md` pessoal:

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp e qualquer outro ambiente compatível com agent-skills</strong></summary>

Funciona com qualquer ambiente que leia Agent Skills. Troque `-a <agent>` pelo seu.

### Instalar

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # todos os projetos
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

Abra um novo chat do agente e digite `/i-have-adhd`.

Sem a CLI, copie a pasta da skill para o caminho verificado pelo seu agente:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. Use .agents/skills no OpenCode ou o caminho próprio do agente
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### Verificar

```bash
npx skills list
npx skills ls -g    # se instalado globalmente
```

### Atualizar

```bash
npx skills update i-have-adhd
npx skills update -g    # se instalado globalmente
```

### Desinstalar

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # se instalado globalmente
```

### Sempre ativo (opcional)

Cole isto no arquivo de regras persistentes do agente. Cursor: **Settings → Rules → User Rules**, ou uma regra de projeto em `.cursor/rules/` com `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## Estilo de resposta

A pessoa que lê tem TDAH. Estruture cada resposta para que ela possa agir:

1. Comece pela resposta ou próxima ação: comando, caminho ou trecho de código primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que possa ser feita em menos de dois minutos.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno ("etapa 3 de 5 concluída").
6. Dê estimativas de tempo em unidades concretas, nunca "um pouco".
7. Após uma alteração, mostre o que agora funciona.
8. Erros: informe local, causa e correção, sem drama.
9. Limite listas a 5 itens.
10. Sem preâmbulo, recapitulação ou despedida.

Exceções: explique por completo quando pedirem. Confirme antes de ações destrutivas. Após três tentativas de correção sem sucesso, pare e identifique a suposição duvidosa. Se o pedido for ambíguo, faça uma pergunta curta.
```
</details>


## Como a ativação funciona

1. **Instalada, mas não invocada.** No Claude Code, Qwen Code e Codex, nada acontece até que você invoque a skill explicitamente. Claude Code e Qwen Code respeitam `disable-model-invocation: true` em `SKILL.md`; o Codex respeita `policy.allow_implicit_invocation: false` em `agents/openai.yaml`. Outros ambientes podem carregar a descrição de cada skill na inicialização e ativá-la por conta própria.
2. **Você a invoca explicitamente.** Digite `/i-have-adhd` no Claude Code ou Qwen Code, ou `$i-have-adhd` no Codex. As regras ficam ativas nessa sessão. "stop adhd mode" ou "normal mode" as desativa.
3. **Você cria `~/.claude/.i-have-adhd-always`** (Claude Code). Um hook `SessionStart` carrega todas as regras desde a primeira mensagem, em toda sessão.
4. **Você adiciona o trecho sempre ativo acima** (outros ambientes). Isso mantém as regras principais no contexto persistente do agente.

No Claude Code, Qwen Code e Codex não há meio-termo: se você não ativou, está desativado.

## Solução de problemas

**`/i-have-adhd` não aparece no preenchimento automático.** Reinicie o agente. O índice de plugins é lido na inicialização.

**A flag de sempre ativo não funciona.** Atualize o plugin (`claude plugin marketplace update i-have-adhd`) e reinicie. Hooks são lidos na inicialização, e a flag exige a versão que inclui `hooks/hooks.json`.

**`claude plugin marketplace add` falha.** Use o formato `owner/repo`. Um caminho local deve apontar para a raiz do repositório, não para `.claude-plugin/`.

**Instalada, mas as respostas ainda têm preâmbulo.** Abra uma nova sessão. Se continuar desviando, torne mais rigoroso o texto em `skills/i-have-adhd/SKILL.md`.

**Quer regras diferentes.** Faça um fork, edite `skills/i-have-adhd/SKILL.md` e troque pela sua cópia:

```bash
claude plugin uninstall i-have-adhd            # remova primeiro a cópia upstream:
claude plugin marketplace remove i-have-adhd   # o fork e o upstream usam o mesmo nome
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Reinicie e invoque `/i-have-adhd` novamente.

**A skill não aparece após `npx skills add`.** Abra um novo chat do agente. Skills são indexadas no início da sessão. Confirme que a pasta foi instalada onde o agente procura (`~/.cursor/skills/` no Cursor, `.agents/skills/` no OpenCode) e que o `name` no frontmatter corresponde ao nome da pasta.
