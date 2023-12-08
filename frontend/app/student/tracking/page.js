'use client'

import { useUserStore } from "@/store/store"
import { useEffect, useState } from "react"
import * as EmailValidator from 'email-validator';

import { AgGridReact } from 'ag-grid-react'; // React Grid Logic

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
    // const code = response.status

    // if (code === 200) {
      // delete row from the table
    // }
    // else {

    // }

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
  const [data, setData] = useState([])
  const [tempData, setTempData] = useState([])

  // logistics state
  const [editing, setEditing] = useState(false)
  const [statusCode, setStatusCode] = useState('')
  const [areEmailsValid, setAreEmailsValid] = useState(true)

  // get initial data
  useEffect(() => {
    const fetchUsers = async () => {
      console.log('sup1')
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      })

      const code = response.status
      setStatusCode(code)

      if (code === 200) {
        const json = await response.json()
        console.log(json)

        setData(json)
      }
    }

    fetchUsers()
      .catch(err => console.log(err, 'from the admin/users page'))
  }, [])

  // validate if data is correct
  const validateEmails = () => {
    if (data && data.some(e => !EmailValidator.validate(e.email))) {
      setAreEmailsValid(false)
    }
    else {
      setAreEmailsValid(true)
    }
  }

  const startEditing = () => {
    setTempData(data)
    setEditing(true)
  }

  // helpers
  const addNewUser = () => {
    startEditing()

    setData([...data, {
      "uin": Math.max(...data.map(e => e.uin)) + 1,
      "first_name": '',
      'last_name': '',
      'm_initial': '',
      'password': '',
      "discord_name": '',
      "user_type": '',
      "username": '',
      "email": '',
    }])
  }

  // TODO: save the data
  const saveData = () => {
    // TODO: create new users

    // TODO: update admin status

    // TODO: update user's details
  }

  // const cancelChanges = () => {
  //   setEditing(false)
  //   setData([...tempData])
  // }

  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">
      <h1 class="text-3xl">Manage Users</h1>

      <div className="flex gap-3">
        <button
          onClick={addNewUser}
          className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded w-42'
        >Add new user (+)</button>

        {
          (editing) ? '' :
            <button
              onClick={startEditing}
              className='bg-purple-500 hover:bg-purple-400 text-white font-bold py-2 px-4 border-b-4 border-purple-700 hover:border-purple-500 rounded w-42'
            >Edit Table (+)</button>
        }

        {
          (!editing) ? '' :
            <button
              onClick={saveData}
              className='bg-green-500 hover:bg-green-400 text-white font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded w-42'
            >Save Changes</button>
        }

        {/* <button TODO:
          onClick={cancelChanges}
          className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded w-42'
        >Cancel Changes</button> */}

        {!areEmailsValid ?
          <span className="text-sm text-red-600">Ensure no emails are empty & all are valid</span> : ''
        }
      </div>

      <div className="ag-theme-quartz h-screen">
        {/* <AgGridReact
          onCellKeyDown={validateEmails}
          rowData={data}
          columnDefs={[
            {
              "field": "uin",
              "headerName": "UIN"
            },
            {
              "field": "username",
              "headerName": "Username"
            },
            {
              "field": "email",
              "headerName": "Email",
              "editable": (params) => editing && !!!params.data.username,
              "cellStyle": (params) => ({ "backgroundColor": (editing && !!!params.data.username) ? '#FFFFE0' : '' })
            },
            {
              "field": 'first_name',
              "editable": editing,
              "headerName": "First Name",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' }
            },
            {
              "field": 'last_name',
              "editable": editing,
              "headerName": "Last Name",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' }
            },
            {
              "field": 'm_initial',
              "editable": editing,
              "headerName": "Middle Initial",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' }
            },
            {
              "field": 'password',
              "editable": editing,
              "headerName": "Password",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' }
            },
            {
              "field": "discord_name",
              "editable": editing,
              "headerName": "Discord Name",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' }
            },
            {
              "field": "user_type",
              "editable": editing,
              "headerName": "User Type",
              "cellStyle": { "backgroundColor": (editing) ? '#FFFFE0' : '' },
              "cellEditor": "agSelectCellEditor",
              "cellEditorParams": {
                "values": ["ADMIN", "USER"]
              }
            },
            {
              "headerName": "Deactivate",
              // "cellRenderer": <button
            },
            {
              "headerName": "Delete",
              "cellRenderer": deleteButton
            }
          ]}
        /> */}
      </div>
    </main>
  )
}
