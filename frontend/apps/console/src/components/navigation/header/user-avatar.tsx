import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "@workspace/ui/components/avatar"

import { User } from "next-auth"

export const UserAvatar = ({ user }: { user: User }) => {

  const initials = user.name
    ?.split(' ')
    ?.map((word) => word[0])
    ?.join('')
    ?.toUpperCase()

  return (
    <Avatar className='size-8 rounded-sm cursor-pointer hover:opacity-80'>
      {user.image && <AvatarImage src={user.image} alt={initials} />}
      <AvatarFallback>{initials}</AvatarFallback>
    </Avatar>
  )
}