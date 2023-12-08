'use client'

import { useState } from 'react'
import Link from 'next/link'
import * as EmailValidator from 'email-validator';

export default function Home() {
  const [email, setEmail] = useState('')
  const [statusCode, setStatusCode] = useState('')

  const sendPasswordResetRequest = async () => {
    console.log('sup2')
    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/auth`, { // TODO: replace url
      // method: 'GET',
      // headers: {
      //   // 'Authorization': 'Basic ' + Buffer.from(username + ":" + password).toString('base64')
      // },
      // body: {
      //   username: username,
      //   password: password,
      // }
    })

    const code = response.status
    setStatusCode(code)
  }

  return (
    <main className="bg-[#500000] h-screen flex items-center justify-center">
      <div className='flex flex-col bg-white w-96 rounded-sm px-4 py-3'>
        <h1 className='font-extrabold text-xl mb-1'>Please reset your password</h1>

        <div className='flex flex-col'>
          <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email on File</label>
          <input type='text' id='email' className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder='Email' value={email} onChange={(e) => setEmail(e.target.value)}/>
        </div>

        <span className='text-sm my-3'>Alternatively: <Link href='/' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">sign in</Link> or <Link href='/signup' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">sign up</Link></span>

        <div className='flex justify-between my-2'>
          <button
            onClick={sendPasswordResetRequest}
            className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded'>Send password reset email</button>
        </div>

        { EmailValidator.validate(email) || email === '' ? '' : '❌ Your email looks incorrect...'}
        { (statusCode === 200) ? '✅ The admin has been notified' : ''}
        { (statusCode != '' && statusCode != 200) ? '❌ There was some error. Please try again later.' : ''}
      </div>
    </main>
  )
}
