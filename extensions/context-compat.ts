export type ContextMessageMarker = Readonly<{
  type?: string;
  role?: string;
  customType?: string;
  content?: string;
}>;

type CompatibleSessionManager = {
  buildSessionContext?: () => { messages: readonly ContextMessageMarker[] };
  buildContextEntries?: () => readonly ContextMessageMarker[];
};

export function contextMessages(
  sessionManager: unknown,
): readonly ContextMessageMarker[] {
  // Context inspection is advisory. If a runtime changes its session-manager
  // API or temporarily cannot build context, report "not present" so the
  // caller can safely re-inject the rules instead of breaking session startup.
  if (sessionManager === null || typeof sessionManager !== "object") {
    return [];
  }

  const compatible = sessionManager as CompatibleSessionManager;

  try {
    if (typeof compatible.buildSessionContext === "function") {
      const messages = compatible.buildSessionContext().messages;
      return Array.isArray(messages) ? messages : [];
    }

    if (typeof compatible.buildContextEntries === "function") {
      const entries = compatible.buildContextEntries();
      return Array.isArray(entries) ? entries : [];
    }
  } catch {
    return [];
  }

  return [];
}

export function latestMarkerIsActive(
  messages: readonly ContextMessageMarker[],
  activeType: string,
  disabledType: string,
): boolean {
  let active = false;

  for (const message of messages) {
    if (message.role !== "custom" && message.type !== "custom_message") {
      continue;
    }

    if (message.customType === activeType) {
      active = true;
    } else if (message.customType === disabledType) {
      active = false;
    }
  }

  return active;
}

/**
 * The content of the newest still-active marker of `activeType`, tracked
 * independently of latestMarkerIsActive's own presence flag: a runtime whose
 * message objects don't expose `content` on this API surface (unverified
 * for every session-manager compat path) should fall back to "no content
 * available" rather than silently reusing a presence check that ignores
 * content. A caller using this for a freshness comparison (e.g. an embedded
 * version tag) should treat `undefined` as "treat as stale, re-inject" --
 * the safe direction to fail in, since the alternative is serving content
 * that might be out of date.
 */
export function latestMarkerContent(
  messages: readonly ContextMessageMarker[],
  activeType: string,
  disabledType: string,
): string | undefined {
  let content: string | undefined;

  for (const message of messages) {
    if (message.role !== "custom" && message.type !== "custom_message") {
      continue;
    }

    if (message.customType === activeType) {
      content = message.content;
    } else if (message.customType === disabledType) {
      content = undefined;
    }
  }

  return content;
}
