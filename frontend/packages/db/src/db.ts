import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

// Create the Neon HTTP client using your DATABASE_URL
const sql = neon(process.env.DATABASE_URL!);

// Instantiate Drizzle with your schema
export const db = drizzle(sql, { schema });