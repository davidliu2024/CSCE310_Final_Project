'use client'

import { useState } from 'react'
import Link from 'next/link'

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
    <main className="bg-[#500000] h-screen flex items-center justify-center">
      <div className='flex flex-col bg-white w-96 rounded-sm px-4 py-3'>
        <h1 className='font-extrabold text-xl mb-1'>Please sign in</h1>

        <div className='flex flex-col'>
          <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Username</label>
          <input type='text' id='username' className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder='Username' value={username} onChange={(e) => setUsername(e.target.value)}/>
        </div>
        <div className='flex flex-col my-3'>
          <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
          <input type='text' id='password' className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)}/>
        </div>

        <span className='text-sm'>Alternatively: <Link href='/signup' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">sign up</Link> or <Link href='/resetpass' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">reset your password</Link></span>
        
        <div className='flex justify-between my-4'>
          <button className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded' onClick={signInAsStudent}>Sign in as student</button>
          <button className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded'>Sign in as admin</button>
        </div>
      </div>
    </main>
  )
}
