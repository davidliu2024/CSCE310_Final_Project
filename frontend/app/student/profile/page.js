'use client'

import { useUserStore } from "@/store/store"
import { useEffect, useState } from "react"
import * as EmailValidator from 'email-validator';

import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme

const deleteButton = (props) => {
  const deleteReq = async () => {
    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users/${props.data.uin}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(username + ":" + password).toString('base64')
      }
    })

    console.log(response)

  }

  return (
    <button
      onClick={deleteReq}
      className='bg-red-500 hover:bg-red-400 text-white font-bold px-4 rounded h-10'
    > Delete
    </button>
  )
}

export default function Home() {

  // data
  const globalState = useUserStore()
  console.log("gs", globalState)

  const [tempData, setTempData] = useState([])
  const [editing, setEditing] = useState(false)

  const [statusCode, setStatusCode] = useState('')

  const [data, setData] = useState({
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    email: '',
    discordName: '',
    mInitial: '',
    uin: ''
  })

  useEffect(() => {
    console.log(globalState.details.discord_name, globalState.details.discord_name || '')
    console.log(globalState.details.uin, globalState.details.uin || '')

    setData({
      username: globalState.details.username || '',
      password: globalState.details.password || '',
      firstName: globalState.details.first_name || '',
      lastName: globalState.details.last_name || '',
      email: globalState.details.email || '',
      discordName: globalState.details.discord_name || '',
      mInitial: globalState.details.m_initial || '',
      uin: globalState.details.uin || ''
    })
  }, [])

  // logistics state
  const startEditing = () => {
    setTempData({...data})
    setEditing(true)
  }

  const cancelChanges = async () => {
    setData({...tempData})
    setEditing(false)
  }

  const saveData = async () => {
      console.log('sup1')
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(username + ":" + password).toString('base64'),
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          username: username,
          password: password,
          first_name: firstName,
          last_name: lastName,
          email: email,
          discord_name: discord_name,
          m_initial: mInitial,
          uin: uin
        })
      })
  
      const code = response.status
      setStatusCode(code)
      setEditing(false)
  }

  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">
      <h1 className="text-3xl">Profile Info</h1>

      <div className="ag-theme-quartz h-screen">

        <div className='flex flex-col'>
          <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Username</label>
          <input
            disabled={!editing}
            type='text'
            id='username'
            className={`${editing ? 'bg-gray-50' : ''} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Username'
            value={data.username}
            onChange={(e) => setData({...data, username: e.target.value})}
          />

        </div>
        <div className='flex flex-col my-3'>
          <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
          <input
            disabled={!editing}
            type='text'
            id='password'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Password'
            value={data.password}
            onChange={(e) => setData({...data, password: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="first_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">First Name</label>
          <input
            disabled={!editing}
            type='text'
            id='first_name'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='First Name'
            value={data.firstName}
            onChange={(e) => setData({...data, firstName: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="last_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Last Name</label>
          <input
            disabled={!editing}
            type='text'
            id='last_name'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Last Name'
            value={data.lastName}
            onChange={(e) => setData({...data, lastName: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email</label>
          <input
            disabled={!editing}
            type='text'
            id='email'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Email'
            value={data.email}
            onChange={(e) => setData({...data, email: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="discord_name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Discord Handle</label>
          <input
            disabled={!editing}
            type='text'
            id='discord_name'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Discord Name'
            value={data.discordName}
            onChange={(e) => setData({...data, discordName: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="middleI" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Middle Initial</label>
          <input
            disabled={!editing}
            type='text'
            id='middleI'
            className={`${!editing ? '' : 'bg-gray-50'} border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='Middle Initial'
            value={data.mInitial}
            onChange={(e) => setData({...data, mInitial: e.target.value})}
          />
        </div>

        <div className='flex flex-col my-3'>
          <label htmlFor="uin" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">UIN</label>
          <input
            type='text'
            id='uin'
            className={`border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500`}
            placeholder='uin'
            value={data.uin}
            disabled={true}
          />
        </div>


      <div className="flex gap-3 mb-1">
        {
          (editing) ? '' :
            <button
              onClick={startEditing}
              className='bg-purple-500 hover:bg-purple-400 text-white font-bold py-2 px-4 border-b-4 border-purple-700 hover:border-purple-500 rounded w-42'
            >Edit</button>
        }

        {
          (!editing) ? '' :
            <button
              disabled={!EmailValidator.validate(data?.email)}
              onClick={saveData}
              className='bg-green-500 hover:bg-green-400 text-white font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded w-42'
            >Save Changes</button>
        }

        {
          (!editing) ? '' :
            <button
              onClick={cancelChanges}
              className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded w-42'
            >Cancel Changes</button>
        }
      </div>

        {(data?.email != '' && !EmailValidator.validate(data.email)) ? '❌ Please enter a valid email' : ''}

        {(statusCode === 202) ? '✅ Fields updated successfully.' : ''}
        {(statusCode !== '' && statusCode !== 202) ? '❌ There is some error. Please try again.' : ''}

      </div>
    </main>
  )
}
