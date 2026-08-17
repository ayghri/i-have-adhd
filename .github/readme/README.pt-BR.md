<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Respostas amigáveis para quem tem TDAH. Sem precisar de diagnóstico!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="Licença"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <strong title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</strong> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a>
</p>


## Instalação

🔗 [Instruções de instalação](../install/INSTALL.pt-BR.md)

## O que ela faz

Uma skill para o seu assistente de código que impede que ele enterre a resposta. Ação primeiro. Passos numerados. Nada de "Espero ter ajudado!"


## O que muda


<table>
<tr>
<td width="50%">

## Antes

> Ótima pergunta! Deixa eu pensar sobre isso. Seu fluxo de autenticação tem algumas partes envolvidas: o middleware, a verificação do token e o tratamento do cookie. Olhando o `src/auth.ts`, a função `verifyToken` (por volta das linhas 42-58) parece estar usando uma API antiga do `jsonwebtoken`. Uma abordagem seria atualizar o pacote e reescrever essa função. Depois da mudança, você vai querer rodar os testes de autenticação para confirmar que nada quebrou. Aliás, talvez valha a pena revisar as versões das suas dependências no geral. Espero ter ajudado! Me avise se quiser se aprofundar.

</td>

<td width="50%">

## Depois

> Rode `npm install jsonwebtoken@latest` e depois edite `src/auth.ts:42`.
>
> 1. Abra `src/auth.ts`
> 2. Substitua `verifyToken` (linhas 42–58) pelo trecho abaixo
> 3. Rode `npm test -- auth.spec.ts`
>
> Próximo passo: cole a primeira linha de falha se algum teste quebrar.

</td>
</tr>
</table>


## As regras

10 regras. Texto completo no [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Comece pela próxima ação.
2. Numere tarefas de múltiplos passos.
3. Termine com um próximo passo concreto.
4. Corte as tangentes.
5. Reafirme o estado atual a cada turno.
6. Estimativas de tempo específicas (minutos, não "um pouco").
7. Deixe as conquistas visíveis.
8. Erros relatados de forma objetiva.
9. Limite listas a 5 itens.
10. Sem preâmbulo. Sem recapitulação. Sem frases de encerramento.

## Personalize

Faça um fork, edite `skills/i-have-adhd/SKILL.md` e troque pela sua cópia:

```bash
claude plugin uninstall i-have-adhd            # remova a cópia do upstream primeiro:
claude plugin marketplace remove i-have-adhd   # fork e upstream compartilham o mesmo nome
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Reinicie o Claude Code e invoque `/i-have-adhd` de novo.

## Créditos

Baseado livremente em *The Adult ADHD Tool Kit*, de J. Russell Ramsay e Anthony L. Rostain. Adaptado para como um LLM deveria responder, não para como uma pessoa deveria organizar o dia.

## Licença

MIT.

Dê uma ⭐ se isso te poupou de rolar a tela por mais um "Ótima pergunta!"
