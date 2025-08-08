import { RunOptions, RunResult } from "./types.js";
import { compile } from "./compile.js";
import { validate } from "./validate.js";

export async function run(source: string, options: RunOptions = {}): Promise<RunResult> {
  const v = validate(source);
  if (!v.ok) throw new Error("Invalid LMTagScript: " + JSON.stringify(v.diagnostics));
  const c = compile(source);
  // Execução simulada: no futuro, plugar runners para @tool, @db etc.
  const logs = [
    "validate: ok",
    `compile: task='${(c.json as any).task}'`
  ];
  return { logs, result: c.json };
}
