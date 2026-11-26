import {
  contextMessages,
  latestMarkerContent,
  latestMarkerIsActive,
} from "../extensions/context-compat";

const ACTIVE = "i-have-adhd-rules";
const DISABLED = "i-have-adhd-disabled";

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) {
    throw new Error(message);
  }
}

const ompMessages = [{ role: "custom", customType: ACTIVE }];
const ompManager = {
  buildSessionContext: () => ({ messages: ompMessages }),
  buildContextEntries: () => {
    throw new Error("Pi fallback must not run when OMP API is available");
  },
};
assert(
  contextMessages(ompManager) === ompMessages,
  "OMP session-context messages were not returned",
);

const piEntries = [{ type: "custom_message", customType: ACTIVE }];
const piManager = {
  buildContextEntries: () => piEntries,
};
assert(
  contextMessages(piManager) === piEntries,
  "Pi context entries were not returned",
);

assert(
  contextMessages({}).length === 0,
  "Unsupported session managers must fail open",
);

assert(
  contextMessages({
    buildSessionContext: () => {
      throw new Error("temporary context failure");
    },
  }).length === 0,
  "Context failures must fail open",
);

assert(
  latestMarkerIsActive(
    [
      { role: "custom", customType: ACTIVE },
      { role: "custom", customType: DISABLED },
      { role: "custom", customType: ACTIVE },
    ],
    ACTIVE,
    DISABLED,
  ),
  "OMP marker ordering was not preserved",
);

assert(
  !latestMarkerIsActive(
    [
      { type: "custom_message", customType: ACTIVE },
      { type: "custom_message", customType: DISABLED },
    ],
    ACTIVE,
    DISABLED,
  ),
  "Pi marker ordering was not preserved",
);

assert(
  !latestMarkerIsActive(
    [
      { role: "user", customType: ACTIVE },
      { type: "message", customType: ACTIVE },
    ],
    ACTIVE,
    DISABLED,
  ),
  "Ordinary messages must not activate the rules",
);

// TASK 9 (Optimize Context Injection): latestMarkerContent backs the
// hash-based staleness check in extensions/i-have-adhd.ts. It has to track
// content independently of latestMarkerIsActive's own presence flag -- see
// that function's doc comment for why the two must not be derived from
// each other.

assert(
  latestMarkerContent(
    [
      { role: "custom", customType: ACTIVE, content: "old" },
      { role: "custom", customType: ACTIVE, content: "new" },
    ],
    ACTIVE,
    DISABLED,
  ) === "new",
  "The newest active marker's content should win over an earlier one",
);

assert(
  latestMarkerContent(
    [
      { role: "custom", customType: ACTIVE, content: "old" },
      { role: "custom", customType: DISABLED },
    ],
    ACTIVE,
    DISABLED,
  ) === undefined,
  "A later disabled marker must cancel an earlier active marker's content",
);

assert(
  latestMarkerContent(
    [
      { role: "custom", customType: ACTIVE, content: "old" },
      { role: "custom", customType: DISABLED },
      { role: "custom", customType: ACTIVE, content: "fresh" },
    ],
    ACTIVE,
    DISABLED,
  ) === "fresh",
  "An active marker after a disabled one must win again",
);

assert(
  latestMarkerContent([], ACTIVE, DISABLED) === undefined,
  "No messages means no content",
);

assert(
  latestMarkerContent(
    [{ role: "custom", customType: ACTIVE }],
    ACTIVE,
    DISABLED,
  ) === undefined,
  "A marker with no content field at all must report undefined, not throw or coerce",
);

console.log("Pi/OMP context compatibility checks passed");
