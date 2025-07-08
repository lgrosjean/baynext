import { Button } from "@workspace/ui/components/button";
import { Card, CardContent } from "@workspace/ui/components/card";

import NewsletterForm from "@/components/newsletter-form"
import Header from "@/components/header";

export default function Home() {

  return (
    <main className="min-h-screen text-white">
      <Header />
      <section className="container mx-auto py-24 text-center">
        <h1 className="text-4xl md:text-[48px] leading-none font-semibold mb-6 text-secondary">BayNext</h1>
        <p className="text-lg font-thin md:text-xl max-w-2xl mx-auto mb-10 text-zinc-300 subpixel-antialiased">
          Open-source platform to deploy and scale your Mix Marketing Models with ease.
        </p>
        <Button className="text-base rounded-full p-6">
          Get Started
        </Button>
      </section>

      <section className="py-10 mx-20">
        <div className="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-[#2a2a3d] border-secondary">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold mb-2 text-secondary">Plug & Play</h3>
              <p className="text-zinc-300">Deploy in minutes using our open architecture powered by Google Meridian.</p>
            </CardContent>
          </Card>
          <Card className="bg-[#2a2a3d] border-secondary">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold mb-2 text-secondary">Open-Source First</h3>
              <p className="text-zinc-300">Start free and scale to cloud when you need to, with full transparency.</p>
            </CardContent>
          </Card>
          <Card className="bg-[#2a2a3d] border-secondary">
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold mb-2 text-secondary">Built for Marketers</h3>
              <p className="text-zinc-300">A clean console experience and actionable insights from day one.</p>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="container mx-auto py-20 text-center">
        <h2 className="text-2xl font-semibold mb-4 text-[#00FFF7]">Join the newsletter</h2>
        <p className="text-zinc-400 mb-6">Stay in the loop as we launch Baynext OSS & Cloud</p>
        <NewsletterForm />
      </section>

      <footer className="border-t border-t-primary text-zinc-400 py-10 text-center">
        <p>© {new Date().getFullYear()} Baynext. Reach us at <a className="underline text-[#00FFF7]" href="mailto:contact@baynext.tech">contact@baynext.tech</a></p>
      </footer>
    </main>
  );
}
