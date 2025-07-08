import { pgTable, varchar, timestamp } from "drizzle-orm/pg-core";

export const subscribers = pgTable("subscribers", {
    email: varchar("email", { length: 255 }).primaryKey(),
    subscribedAt: timestamp("subscribed_at").defaultNow(),
  });
  