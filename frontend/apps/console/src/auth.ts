
// https://dev.to/jamescroissant/user-authentication-with-authjs-in-nextjs-app-router-424k

import NextAuth, { type DefaultSession } from "next-auth"
import GitHub from "next-auth/providers/github"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import Credentials from "next-auth/providers/credentials"
import { db } from "@workspace/db/client";
import { users } from "@workspace/db/schema"

// See: https://authjs.dev/getting-started/typescript
declare module "next-auth" {
  /**
   * Returned by `auth`, `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
   */
  interface Session {
    user: {
      /** The user's id. */
      id: string
      /**
       * By default, TypeScript merges new interface properties and overwrites existing ones.
       * In this case, the default session user properties will be overwritten,
       * with the new ones defined above. To keep the default session user properties,
       * you need to add them back into the newly declared interface.
       */
    } & DefaultSession["user"]
  }
}
 
export const { auth, handlers, signIn, signOut } = NextAuth({
  session: { strategy: "jwt" },
  pages: {
    signIn: "/login",
    // signOut: "/auth/signout",
    // error: "/auth/error", // Error code passed in query string as ?error=
  },
  adapter: DrizzleAdapter(db),
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    Credentials({
        // You can specify which fields should be submitted, by adding keys to the `credentials` object.
        // e.g. domain, username, password, 2FA token, etc.
        credentials: {
          email: {},
          password: {},
        },
        authorize: async (credentials) => {
          let user = null
   
          // logic to salt and hash password
          const pwHash = saltAndHashPassword(credentials.password)
   
          // logic to verify if the user exists
          user = await getUserFromDb(credentials.email, pwHash)
   
          if (!user) {
            // No user found, so this is their first attempt to login
            // Optionally, this is also the place you could do a user registration
            throw new Error("Invalid credentials.")
          }
   
          // return user object with their profile data
          return user
        },
      })
    ],
    callbacks: {
      //  By default, the `id` property does not exist on `token` or `session`. See the [TypeScript](https://authjs.dev/getting-started/typescript) on how to add it.
      jwt({ token, user, account, profile }) {
        if (user) { // User is available during sign-in
          token.id = user.id
        }
        // if (profile) {
        //   token.accessToken = profile.access_token
        //   token.id = profile.id
        // }
        return token
      },
      // https://authjs.dev/guides/extending-the-session#with-jwt
      session({ session, token, user }) {
        session.user.id = token.id as string
        return session
      },
      authorized({ auth, request: { nextUrl } }) {
        const isLoggedIn = !!auth?.user;
        const isOnDashboard = nextUrl.pathname.startsWith('/app');
        if (isOnDashboard) {
          if (isLoggedIn) return true;
          return false; // Redirect unauthenticated users to login page
        }
        return true;
      }
    },
  })