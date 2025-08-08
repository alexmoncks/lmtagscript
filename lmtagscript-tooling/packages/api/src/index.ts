import Fastify from "fastify";
import { validate, compile, run } from "@lmtagscript/core";

const app = Fastify({ logger: true });

app.post("/validate", async (req, res) => {
  const { source } = (req.body as any) ?? {};
  if (!source) return res.code(400).send({ error: "Missing 'source'" });
  return validate(source);
});

app.post("/compile", async (req, res) => {
  const { source } = (req.body as any) ?? {};
  if (!source) return res.code(400).send({ error: "Missing 'source'" });
  return compile(source);
});

app.post("/run", async (req, res) => {
  const { source, options } = (req.body as any) ?? {};
  if (!source) return res.code(400).send({ error: "Missing 'source'" });
  const result = await run(source, options);
  return result;
});

const port = Number(process.env.PORT || 3000);
app.listen({ port, host: "0.0.0.0" }).then(() => console.log(`API on :${port}`));
