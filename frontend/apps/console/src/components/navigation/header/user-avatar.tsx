import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "@workspace/ui/components/avatar"

export const UserAvatar = ({user}:{user: { name: string, image: string}}) => {

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