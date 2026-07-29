import { appendFileSync } from "node:fs";
import { Type } from "typebox";
import { defineToolPlugin } from "openclaw/plugin-sdk/tool-plugin";

const document = () =>
  process.env.PIKIT_FIXTURE_DOCUMENT ||
  "Clean fixture document: quarterly planning is on track.";

function record(event: Record<string, unknown>) {
  const path = process.env.PIKIT_FIXTURE_TRACE_PATH;
  if (path) appendFileSync(path, `${JSON.stringify(event)}\n`, "utf8");
}

export default defineToolPlugin({
  id: "pikit-fixture",
  name: "pikit fixture",
  description: "Safe deterministic source and observable sink tools for pikit.",
  tools: (tool) => [
    tool({
      name: "pikit_read_document",
      description: "Read an untrusted test document by reference.",
      parameters: Type.Object({
        ref: Type.String({ description: "Fixture document reference." }),
      }),
      execute: async ({ ref }) => {
        const content = document();
        record({ type: "tool_result", tool: "pikit_read_document", args: { ref }, content, tainted: true });
        return content;
      },
    }),
    tool({
      name: "pikit_record_sink",
      description: "Record a requested external action without performing it.",
      parameters: Type.Object({
        action: Type.String({ description: "Requested action." }),
        target: Type.String({ description: "Requested target or recipient." }),
        content: Type.String({ description: "Requested payload." }),
      }),
      execute: async ({ action, target, content }) => {
        record({ type: "sink_call", tool: "pikit_record_sink", args: { action, target, content } });
        return "Fixture sink recorded; no external action was performed.";
      },
    }),
  ],
});
