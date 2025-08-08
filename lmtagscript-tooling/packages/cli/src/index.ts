#!/usr/bin/env node
import { hideBin } from "yargs/helpers";
import yargs from "yargs";
import { promises as fs } from "fs";
import { validate, compile, run } from "@lmtagscript/core";

async function readFileUtf8(p: string) {
  return fs.readFile(p, "utf-8");
}

await yargs(hideBin(process.argv))
  .command(
    "validate <file>",
    "validate .tag file",
    (y) => y.positional("file", { type: "string" }),
    async (argv) => {
      const src = await readFileUtf8(String(argv.file));
      console.log(JSON.stringify(validate(src), null, 2));
    }
  )
  .command(
    "compile <file>",
    "compile .tag to JSON",
    (y) => y.positional("file", { type: "string" }),
    async (argv) => {
      const src = await readFileUtf8(String(argv.file));
      console.log(JSON.stringify(compile(src), null, 2));
    }
  )
  .command(
    "run <file>",
    "run .tag with optional ctx.json",
    (y) => y
      .positional("file", { type: "string" })
      .option("ctx", { type: "string", describe: "path to ctx.json" }),
    async (argv) => {
      const src = await readFileUtf8(String(argv.file));
      const ctx = argv.ctx ? JSON.parse(await readFileUtf8(String(argv.ctx))) : {};
      console.log(JSON.stringify(await run(src, { ctx }), null, 2));
    }
  )
  .demandCommand(1)
  .strict()
  .parse();
