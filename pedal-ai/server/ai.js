import OpenAI from "openai";
import dotenv from "dotenv";
import { catalog } from "./catalog.js";
import { logSize } from "./analytics.js";

dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function processMessage(message, session) {

  const lower = message.toLowerCase();

  // ==========================
  // RULE BASED COMMERCE LOGIC
  // ==========================

  // Greeting
  if (lower.includes("halo, selamat pagi, selamat siang, selamat sore, selamat malam") || lower.includes("hai")) {
    return "Halo 👋 Selamat datang di Pedal Acid! Silakan beri tahu berat badan Anda agar kami bisa rekomendasikan size yang tepat.";
  }

  // Stok
  if (lower.includes("stok")) {
    return `
Stok tersedia:
XXS: ${catalog.stock.XXS}
XS: ${catalog.stock.XS}
S: ${catalog.stock.S}
`;
  }

  // Warna
  if (lower.includes("warna")) {
    return "Saat ini tersedia warna Hitam.";
  }

  // Tangkap berat badan
  const weightMatch = message.match(/\d+/);
  if (weightMatch) {
    const weight = parseInt(weightMatch[0]);
    session.weight = weight;

    const found = catalog.sizes.find(
      s => weight >= s.min && weight <= s.max
    );

    if (found) {
      session.selectedSize = found.size;
      logSize(found.size);
      return `Untuk berat ${weight} kg, kami sarankan size ${found.size}. Stok tersedia: ${catalog.stock[found.size]}. Mau lanjut order?`;
    } else {
      return "Mohon maaf, berat tersebut belum masuk range size yang tersedia.";
    }
  }

  // Order
  if (lower.includes("ambil") || lower.includes("order") || lower.includes("lanjut")) {

    if (!session.selectedSize) {
      return "Sebelum order, mohon beri tahu berat badan Anda terlebih dahulu.";
    }

    const size = session.selectedSize;

    if (catalog.stock[size] > 0) {
      catalog.stock[size]--;

      return `
✅ Ringkasan Order:
Produk: ${catalog.product}
Warna: ${catalog.color}
Size: ${size}

Stok tersisa: ${catalog.stock[size]}

Silahkan klik WhatsApp untuk melanjutkan pembayaran.
`;
    } else {
      return "Mohon maaf, stok size tersebut habis.";
    }
  }

  // ==========================
  // LLM FALLBACK (SMART CHAT)
  // ==========================

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `
Anda adalah AI Sales Assistant brand Pedal Acid.
Jawab dengan ramah dan natural.
Jangan mengarang stok atau warna.
Data resmi:
Produk: Jersey Vaya con Fuerza
Warna: Hitam
Size: XXS, XS, S
`
        },
        {
          role: "user",
          content: message
        }
      ]
    });

    return response.choices[0].message.content;

  } catch (error) {
    console.error("LLM ERROR:", error);
    return "Mohon maaf, sistem sedang mengalami kendala.";
  }
}