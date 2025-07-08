import {
  BadgeCheck,
  Bell,
  CreditCard,
  LogOut,
  Sparkles,
} from "lucide-react"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@workspace/ui/components/dropdown-menu"

import { UserAvatar } from "./user-avatar"

import { signOut } from "@/auth"

const menuItems = [
  {
    title: "Account",
    icon: BadgeCheck,
    url: "#",
  },
  {
    title: "Billing",
    icon: CreditCard,
    url: "#",
  },
  {
    title: "Notifications",
    icon: Bell,
    url: "#",
  },
]

export function NavUser({ user }: { user: { name: string; email: string, image: string } }) {

  return (
    <DropdownMenu>
      <DropdownMenuTrigger >
          <UserAvatar user={user}/>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-sm"
        side={"bottom"}
        align="end"
        sideOffset={4}
      >
        <DropdownMenuLabel className="p-0 font-normal">
          <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
            <UserAvatar user={user}/>
            <div className="grid flex-1 text-left text-sm leading-tight">
              <span className="truncate font-medium">{user?.name}</span>
              <span className="truncate text-xs">{user?.email}</span>
            </div>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            <Sparkles />
            Upgrade to Pro
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          {menuItems.map((item) => (
            <DropdownMenuItem key={item.title}>
              <item.icon />
              {item.title}
            </DropdownMenuItem>
          ))}
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <form
          action={async () => {
            "use server"
            await signOut({ redirectTo: "/login" })
          }}
        >
          <DropdownMenuItem asChild>

            <button type="submit" className="w-full">
              <LogOut />
              Log out
            </button>

          </DropdownMenuItem></form>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
