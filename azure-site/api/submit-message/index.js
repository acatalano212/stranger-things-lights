const { TableClient } = require("@azure/data-tables");

module.exports = async function (context, req) {
  const headers = { "Content-Type": "application/json" };

  if (req.method === "OPTIONS") {
    context.res = { status: 204, headers };
    return;
  }

  try {
    const body = req.body;
    if (!body || !body.message) {
      context.res = { status: 400, headers, body: JSON.stringify({ error: "No message provided" }) };
      return;
    }

    let message = body.message.toUpperCase().trim();

    if (!/^[A-Z ]+$/.test(message)) {
      context.res = { status: 400, headers, body: JSON.stringify({ error: "A-Z and spaces only" }) };
      return;
    }
    if (message.length > 50) {
      context.res = { status: 400, headers, body: JSON.stringify({ error: "Max 50 characters" }) };
      return;
    }

    const connStr = process.env.STORAGE_CONNECTION_STRING;
    if (!connStr) {
      context.res = { status: 500, headers, body: JSON.stringify({ error: "Storage not configured" }) };
      return;
    }

    const client = TableClient.fromConnectionString(connStr, "messages");
    await client.createTable().catch(() => {});

    // Reject if a message is already pending (less than 30s old)
    try {
      const existing = await client.getEntity("pending", "current");
      const age = (Date.now() - new Date(existing.submittedAt).getTime()) / 1000;
      if (age < 30) {
        context.res = {
          status: 429, headers,
          body: JSON.stringify({ error: "A message is already being sent to the lights. Try again in a moment!" })
        };
        return;
      }
    } catch (e) {
      // No existing message — good
    }

    await client.upsertEntity({
      partitionKey: "pending",
      rowKey: "current",
      text: message,
      submittedAt: new Date().toISOString()
    });

    context.res = { status: 200, headers, body: JSON.stringify({ success: true, message }) };
  } catch (e) {
    context.log.error("submit-message error:", e);
    context.res = { status: 500, headers, body: JSON.stringify({ error: "Internal error" }) };
  }
};
