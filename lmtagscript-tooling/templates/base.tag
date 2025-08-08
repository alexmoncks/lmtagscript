TASK: Captar e qualificar lead
ACTION: Receber webhook, validar e criar/atualizar contato no CRM; classificar e agendar follow-up
GOAL: Lead qualificado com próximo passo definido e registro auditável

@tool:webhook { endpoint: "/lead" }
@tool:crm { operation: "upsert", table: "contacts" }
@tool:scheduler { operation: "create_task", assignee: "sales" }

IF lead.email IS NOT NULL THEN
  @tool:crm { operation: "upsert", payload: lead }
  @tool:scheduler { operation: "create_task", payload: { due_in: "24h", note: "Retornar ao lead" } }
ELSE
  ON ERROR
    TASK: Registrar falha
    ACTION: Enviar alerta no Slack e guardar payload em dead-letter
    GOAL: Não perder lead; acionar correção de fonte
END

LOOPGUARD { max_depth: 2, allow_repeat: false }
