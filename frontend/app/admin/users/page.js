'use client'

import { useUserStore } from "@/store/store"
import { useEffect, useState } from "react"
import * as EmailValidator from 'email-validator';

import { AgGridReact } from 'ag-grid-react'; // React Grid Logic

import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme

const deactivateButton = (props) => {
  const deactivateReq = async () => {
    if (props.globalState.username === props.data.username) {
      props.setStatusCode(1000)
    }
    else {
      // update in DB
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users/${props.data.uin}/deactivate`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(props.globalState.username + ":" + props.globalState.password).toString('base64')
        }
      })

      const code = response.status
      props.setStatusCode(code)

      // update locally
      const deactivatedRow = props.theData.find(e => e.uin === props.data.uin)
      const newRow = { ...deactivatedRow, user_type: "DEACTIVATED" }
      const restOfData = props.theData.filter(e => e.uin !== props.data.uin)
      props.setData([...restOfData, newRow])
    }
  }

  const reactivateReq = async () => {
    console.log('reactivating')
    if (props.globalState.username === props.data.username) {
      props.setStatusCode(1000)
    }
    else {
      // update in DB
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users/${props.data.uin}/activate`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(props.globalState.username + ":" + props.globalState.password).toString('base64')
        }
      })

      console.log('reactinvaitng 2')
      const code = response.status
      props.setStatusCode(code)

      // update locally
      const activatedRow = props.theData.find(e => e.uin === props.data.uin)
      const newRow = { ...activatedRow, user_type: "USER" }
      const restOfData = props.theData.filter(e => e.uin !== props.data.uin)
      props.setData([...restOfData, newRow])
    }
  }

  return (
    props.data.user_type === "DEACTIVATED" ?
      <button
        onClick={reactivateReq}
        className='bg-green-500 hover:bg-green-400 text-white font-bold px-4 rounded h-10'
      >
        Reactivate
      </button>
      :
      <button
        onClick={deactivateReq}
        className='bg-orange-500 hover:bg-orange-400 text-white font-bold px-4 rounded h-10'
      >
        Deactivate
      </button>
  )

}

const deleteButton = (props) => {
  const deleteReq = async () => {
    if (props.globalState.username === props.data.username) {
      props.setStatusCode(1100)
    }
    else {
      // update locally
      const restOfData = props.theData.filter(e => e.uin !== props.data.uin)
      props.setData([...restOfData])

      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/users/${props.data.uin}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(props.globalState.username + ":" + props.globalState.password).toString('base64')
        }
      })

      const code = response.status
      props.setStatusCode(code)

      console.log('res: ', response)
    }
  }

  return (
    <button
      onClick={deleteReq}
      className='bg-red-500 hover:bg-red-400 text-white font-bold px-4 rounded h-10'
    >
      Delete
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
    console.log('fetching :)')
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
    // 0. get the new users
    const uins = data.map(e => e.uin)
    console.log(uins)

    // TODO: update admin status

    // TODO: update user's details
  }

  // const cancelChanges = () => {
  //   setEditing(false)
  //   setData([...tempData])
  // }

  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">
      <h1 className="text-3xl">Manage Users</h1>

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
        {
          statusCode === 800 ?
            <span className="text-sm text-red-600">❌ Deactivate user failed</span> : ''
        }
        {
          statusCode === 900 ?
            <span className="text-sm text-red-600">❌ Delete user failed</span> : ''
        }
        {
          statusCode === 1000 ?
            <span className="text-sm text-red-600">❌ Cannot deactivate yourself</span> : ''
        }
        {
          statusCode === 1100 ?
            <span className="text-sm text-red-600">❌ Cannot delete yourself</span> : ''
        }
      </div>

      <div className="ag-theme-quartz h-screen">
        <AgGridReact
          onCellKeyDown={validateEmails}
          rowData={data}
          // defaultColDef={{
          //   cellStyle: () => ({
          //     display: "flex",
          //     alignItems: "center",
          //     justifyContent: "center"
          //   })
          // }}

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
              "cellRenderer": deactivateButton,
              "cellRendererParams": {
                "setStatusCode": setStatusCode,
                "setData": setData,
                "theData": data,
                "globalState": globalState
              }
            },
            {
              "headerName": "Delete",
              "cellRenderer": deleteButton,
              "cellRendererParams": {
                "setStatusCode": setStatusCode,
                "setData": setData,
                "theData": data,
                "globalState": globalState
              }
            }
          ]}
        />
      </div>
    </main>
  )
}
