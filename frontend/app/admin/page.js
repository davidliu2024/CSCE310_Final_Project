'use client'

import { useState } from 'react'
import UserProfile from './users/page'

export default function Home() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  // todo: user authentication
  const signInAsStudent = async () => {
    fetch(`${process.env.BASE_PATH}auth/`, {
      headers: {
        'Authorization': 'Basic ' + Buffer.from(username + ":" + password).toString('base64')
      }
    })
    .then((res, err) => {

    })
  }

  return (
      <UserProfile />
  )
}
