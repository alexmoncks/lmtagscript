import { CompileResult } from "./types.js";

// TODO: parser/AST reais. Placeholder convertendo blocos-chave em JSON simples.
export function compile(source: string): CompileResult {
  const toBlock = (key: string) => (source.match(new RegExp(`${key}:(.*?)(\n\n|$)`, "is"))?.[1] || "").trim();
  const ast = {
    task: toBlock("TASK"),
    action: toBlock("ACTION"),
    goal: toBlock("GOAL"),
    refs: Array.from(source.matchAll(/@([\w:-]+)\s*\{([^}]*)}/g)).map(([, ref, body]) => ({ ref, body: body.trim() }))
  };
  const json = {
    type: "LMTagScript",
    version: "0.1",
    task: (ast as any).task,
    action: (ast as any).action,
    goal: (ast as any).goal,
    refs: (ast as any).refs
  };
  return { ast, json, warnings: [] };
}
