<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Respuestas adaptadas para TDAH. ¡No se necesita diagnóstico de TDAH!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/aixinwudi/i-have-adhd-cn?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <strong title="Español" aria-label="Español">🇪🇸</strong> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.fa.md" title="فارسی" aria-label="فارسی">🇮🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a>
</p>


## Instalación

Copia/pega en tu línea de comandos:

```text
Install the i-have-adhd skill/plugin from https://github.com/aixinwudi/i-have-adhd-cn, refer to the repo's AGENTS.md for instructions.
```

O 🔗 [consulta las instrucciones de instalación](../../INSTALL.md).

## Qué hace

Una *skill* para tu asistente de código que evita que entierre la respuesta. Acción primero. Pasos numerados. Nada de "¡Espero que esto ayude!".


## Qué cambia


<table>
<tr>
<td width="50%">

## Antes

> ¡Excelente pregunta! Déjame pensarlo. Tu flujo de autenticación tiene varias piezas móviles: el middleware, la verificación del token y el manejo de cookies. Mirando `src/auth.ts`, la función `verifyToken` (alrededor de las líneas 42-58) parece estar usando una API antigua de `jsonwebtoken`. Un enfoque sería actualizar el paquete y reescribir esa función. Después de hacer el cambio, tendrás que ejecutar las pruebas de autenticación para confirmar que nada se rompa. Por cierto, también deberías revisar las versiones de tus dependencias en general. ¡Espero que esto ayude! Avísame si quieres profundizar más.

</td>

<td width="50%">

## Después

> Ejecuta `npm install jsonwebtoken@latest`, luego edita `src/auth.ts:42`.
>
> 1. Abre `src/auth.ts`
> 2. Reemplaza `verifyToken` (líneas 42–58) con el fragmento a continuación
> 3. Ejecuta `npm test -- auth.spec.ts`
>
> Siguiente paso: pega la primera línea que falle si alguna prueba falla.

</td>
</tr>
</table>


## Las reglas

10 reglas. Texto completo en [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Empieza con la siguiente acción.
2. Numera las tareas de varios pasos.
3. Termina con un paso concreto a seguir.
4. Suprime las tangentes.
5. Reafirma el estado en cada turno.
6. Estimaciones de tiempo específicas (minutos, no "un poco").
7. Haz visibles los logros.
8. Errores mostrados de forma directa (matter-of-fact).
9. Limita las listas a 5 elementos.
10. Sin preámbulos. Sin resúmenes. Sin frases de cierre.

## Ajustarlo

Haz un fork, edita `skills/i-have-adhd/SKILL.md`, luego intercambia tu copia:

```bash
claude plugin uninstall i-have-adhd            # elimina la copia original primero:
claude plugin marketplace remove i-have-adhd   # el fork y el original comparten ambos nombres
claude plugin marketplace add <tu-usuario>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Reinicia tu asistente de código y vuelve a invocar `/i-have-adhd`.

## Créditos

Basado libremente en *The Adult ADHD Tool Kit* de J. Russell Ramsay y Anthony L. Rostain. Adaptado para cómo un LLM debería responder, no para cómo un humano debería organizar su día.

## Licencia

[MIT](../../LICENSE).

Dale una estrella ⭐ si te ahorró hacer scroll ignorando un "¡Excelente pregunta!"
