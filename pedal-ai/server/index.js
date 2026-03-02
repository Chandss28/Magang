import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import { v4 as uuidv4 } from "uuid";
import { processMessage } from "./ai.js";
import { getSession } from "./sessionStore.js";
import { logChat, getStats } from "./analytics.js";

dotenv.config();

const app = express();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../client")));

app.post("/chat", async (req, res) => {
  logChat();

  let sessionId = req.headers["session-id"];
  if (!sessionId) {
    sessionId = uuidv4();
  }

  const session = getSession(sessionId);
  const reply = await processMessage(req.body.message, session);

  res.json({ reply, sessionId });
});

app.get("/admin/stats", (req, res) => {
  res.json(getStats());
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Running at http://localhost:${PORT}`);
});