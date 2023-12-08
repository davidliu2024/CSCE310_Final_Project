'use client'

import { useState } from 'react'
import Link from 'next/link'
import * as EmailValidator from 'email-validator';

export default function Home() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')

  const [statusCode, setStatusCode] = useState('')

  const createUser = async () => {
    console.log('sup2')
    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users`, {
      method: 'POST',
      body: {
        username: username,
        password: password,
        first_name: firstName,
        last_name: lastName,
        email: email
      }
    })

    console.log('response: ', response)
    const code = response.status
    setStatusCode(code)
  }

  return (
    <main className="bg-[#500000] h-screen flex items-center justify-center">
      <div className='flex flex-col bg-white w-96 rounded-sm px-4 py-3'>
        <h1 className='font-extrabold text-xl mb-1'>Please sign up</h1>

        <div className='flex flex-col'>
          <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Username</label>
          <input type='text' id='username' className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder='Username' value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className='flex flex-col my-3'>
          <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
          <input
            type='text'
            id='password'
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder='Password'
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="first_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">First Name</label>
          <input
            type='text'
            id='first_name'
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder='First Name'
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)} 
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="last_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Last Name</label>
          <input
            type='text'
            id='last_name'
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder='Last Name'
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email</label>
          <input
            type='text'
            id='email'
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder='Email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <span className='text-sm'>Alternatively: <Link href='/' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">sign in</Link> or <Link href='/resetpass' className="font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">forgot your password</Link></span>

        <div className='flex justify-between my-4'>
          <button
            // disabled={}
            onClick={createUser}
            className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded'>Sign up</button>
        </div>

        { (email !== '' && !EmailValidator.validate(email)) ? '❌ Please enter a valid email' : ''}
        { ([email, username, password, firstName, lastName].some(e => e !== '')) && ([email, username, password, firstName, lastName].some(e => e === '')) ? '❌ All fields are required' : ''}

        { (statusCode === 202) ? '✅ User created - please log in now' : ''}
        { (statusCode !== '' && statusCode !== 202) ? '❌ There is some error. Please try again.' : ''}

      </div>
    </main>
  )
}
