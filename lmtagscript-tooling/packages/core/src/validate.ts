import { ValidateResult } from "./types.js";

// TODO: substituir por parser real do LMTagScript
export function validate(source: string): ValidateResult {
  const diagnostics: ValidateResult["diagnostics"] = [];
  if (!/\bTASK\b/i.test(source)) diagnostics.push({ message: "Missing TASK", code: "E_TASK", severity: "error" });
  if (!/\bACTION\b/i.test(source)) diagnostics.push({ message: "Missing ACTION", code: "E_ACTION", severity: "error" });
  if (!/\bGOAL\b/i.test(source)) diagnostics.push({ message: "Missing GOAL", code: "E_GOAL", severity: "error" });
  return { ok: diagnostics.length === 0, diagnostics };
}
