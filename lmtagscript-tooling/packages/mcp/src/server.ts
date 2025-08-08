#!/usr/bin/env node
import { validate, compile, run } from "@lmtagscript/core";

// MCP-like STDIO JSON-RPC mínimo (genérico)

process.stdin.setEncoding("utf8");
let buffer = "";

process.stdin.on("data", async (chunk) => {
  buffer += chunk;
  let idx;
  while ((idx = buffer.indexOf("\n")) >= 0) {
    const line = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!line) continue;
    try {
      const msg = JSON.parse(line);
      const { id, method, params } = msg;
      let result;
      if (method === "lmtagscript/validate") result = validate(params.source);
      else if (method === "lmtagscript/compile") result = compile(params.source);
      else if (method === "lmtagscript/run") result = await run(params.source, params.options);
      else throw new Error("Method not found");
      process.stdout.write(JSON.stringify({ id, result }) + "\n");
    } catch (err) {
      const e = err instanceof Error ? err : new Error(String(err));
      process.stdout.write(JSON.stringify({ error: { message: e.message } }) + "\n");
    }
  }
});
