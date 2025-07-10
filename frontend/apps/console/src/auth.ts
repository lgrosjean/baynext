
// https://dev.to/jamescroissant/user-authentication-with-authjs-in-nextjs-app-router-424k

import NextAuth, { type DefaultSession,  NextAuthResult } from "next-auth"
import GitHub from "next-auth/providers/github"
import * as jose from 'jose'

// See: https://authjs.dev/getting-started/typescript
declare module "next-auth" {
  /**
   * Returned by `auth`, `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
   */
  interface Session {
    token: string // Added to include token in the session
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
    // token?: string // Add this line to include token in the session
  }
}
 
const authOptions = NextAuth({
  session: { 
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  pages: {
    signIn: "/login",
  },
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
  ],
  // https://authjs.dev/reference/nextjs#callbacks
  callbacks: {
    //  By default, the `id` property does not exist on `token` or `session`. See the [TypeScript](https://authjs.dev/getting-started/typescript) on how to add it.
    async jwt({ token, user, account }) {
      if (user) { // User is available during sign-in
        token.id = user.id
      }
      return token
    },
    // https://authjs.dev/guides/extending-the-session#with-jwt
    // This callback is called whenever a session is checked.
    async session({ session, token, user }) {
      if (token) {
        session.user.id = token.id as string
        
        if (!process.env.AUTH_SECRET) throw new Error('JWT secret not found')
        const secret = jose.base64url.decode(process.env.AUTH_SECRET)
        session.token = await new jose.SignJWT(token)
          .setProtectedHeader({ alg: 'HS256' })
          .sign(secret)
      }
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
});

// https://github.com/nextauthjs/next-auth/discussions/9950
export const handlers: NextAuthResult['handlers'] = authOptions.handlers;
export const auth: NextAuthResult['auth'] = authOptions.auth;
export const signIn: NextAuthResult['signIn'] = authOptions.signIn;
export const signOut: NextAuthResult['signOut'] = authOptions.signOut;