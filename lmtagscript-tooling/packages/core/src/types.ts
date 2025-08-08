export type ValidateResult = {
  ok: boolean;
  diagnostics: Array<{
    message: string;
    line?: number;
    col?: number;
    code?: string;
    severity?: "error" | "warning";
  }>;
};

export type CompileResult = {
  ast: unknown;
  json: unknown;
  warnings: string[];
};

export type RunOptions = { ctx?: Record<string, unknown> };

export type RunResult = {
  logs: string[];
  result: unknown;
};
