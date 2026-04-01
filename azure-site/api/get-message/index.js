const { TableClient } = require("@azure/data-tables");

module.exports = async function (context, req) {
  const headers = { "Content-Type": "application/json" };

  try {
    // Simple device key auth
    const deviceKey = process.env.DEVICE_KEY;
    if (deviceKey) {
      const provided = req.headers["x-device-key"] || req.query.key;
      if (provided !== deviceKey) {
        context.res = { status: 401, headers, body: JSON.stringify({ error: "Unauthorized" }) };
        return;
      }
    }

    const connStr = process.env.STORAGE_CONNECTION_STRING;
    if (!connStr) {
      context.res = { status: 500, headers, body: JSON.stringify({ error: "Storage not configured" }) };
      return;
    }

    const client = TableClient.fromConnectionString(connStr, "messages");

    try {
      const entity = await client.getEntity("pending", "current");
      await client.deleteEntity("pending", "current");
      context.res = { status: 200, headers, body: JSON.stringify({ message: entity.text }) };
    } catch (e) {
      if (e.statusCode === 404) {
        context.res = { status: 200, headers, body: JSON.stringify({ message: null }) };
      } else {
        throw e;
      }
    }
  } catch (e) {
    context.log.error("get-message error:", e);
    context.res = { status: 500, headers, body: JSON.stringify({ error: "Internal error" }) };
  }
};
