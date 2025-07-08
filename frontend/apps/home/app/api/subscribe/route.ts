// app/api/subscribe/route.ts
import { db } from "@/lib/db";
import { subscribers } from "@workspace/drizzle/schema";
import { NextResponse } from "next/server";
import { Resend } from "resend";
import { z } from "zod";

const resend = new Resend(process.env.RESEND_API_KEY);

const formSchema = z.object({
  email: z.string().email(),
});

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { email } = formSchema.parse(body);

    await db.insert(subscribers).values({ email });

    await resend.emails.send({
      from: "Baynext <noreply@baynext.tech>",
      to: [email],
      subject: "Welcome to Baynext 🚀",
      html: `<p>Thanks for joining the newsletter. We'll keep you updated as we launch!</p>`
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: "Invalid request or already subscribed." }, { status: 400 });
  }
}
