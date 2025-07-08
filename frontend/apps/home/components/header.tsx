// apps/homepage/components/header.tsx
import Image from "next/image";
import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
} from "@workspace/ui/components/navigation-menu";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-[#0a0a0a]/90 backdrop-blur-sm border-b border-zinc-800">
      <div className="container mx-auto flex items-center justify-between py-4 px-6">
        <Link href="/">
          <div className="flex items-center gap-2">
            <Image src="/nextbay.png" alt="Baynext Logo" width={32} height={32} />
            {/* <span className="text-xl text-secondary">Baynext</span> */}
          </div>
        </Link>
        <NavigationMenu>
          <NavigationMenuList className="gap-6">
            <NavigationMenuItem>
              <Link href="#" className="text-white hover:text-[#00FFF7] transition-colors">
                Pricing
              </Link>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <Link href="#" className="text-white hover:text-[#00FFF7] transition-colors">
                Docs
              </Link>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <Link href="#" className="text-white hover:text-[#00FFF7] transition-colors">
                Blog
              </Link>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>
    </header>
  );
}
