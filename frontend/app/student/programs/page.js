'use client'

import { useUserStore } from "@/store/store"
import { useEffect, useState, useMemo } from "react"
import * as EmailValidator from 'email-validator';

import { AgGridReact } from 'ag-grid-react'; // React Grid Logic



import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme



export default function Home() {

  // data
  const globalState = useUserStore()
  const [data, setData] = useState([])
  
  const [editing, setEditing] = useState(false)


  // logistics state

  const [statusCode, setStatusCode] = useState('')


  const startEditing = () => {
  
    setEditing(true)
  }
  // get initial data

  const deleteButton = (props) => {
    const deleteReq = async () => {
      console.log(props.data.app_num)

      
      console.log(`https://csce-310-flask-backend-api.onrender.com/applications/${props.data.app_num}`)
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/applications/${props.data.app_num}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      })
  
      const code = response.status
      setStatusCode(code)

      if (code === 200) {
        const json = await response.json()
        console.log(json)
    }

      
  
    }
  
    return (
      <button
        onClick={deleteReq}
        className='bg-red-500 hover:bg-red-400 text-white font-bold px-4 rounded h-10'
      > Delete
      </button>
    )
  }


  
  

  const addNewUser = () => {
    setEditing(true)

    setData([...data, {
      'app_num': '',
      'program_num': '',
      'uncom_cert': '',
      'com_cert': '',
      "purpose_statement": '',
    }])
  }
  useEffect(() => {
    const fetchUsers = async () => {
   
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/applications`, {
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
      .catch(err => console.log(err, 'from the student/programs page'))
  }, [])


  const saveData = async () => {
    console.log('in save')
      for (let entry = 0; entry < data.length; ++entry){
        try {
          let method = 'POST'
          const bodyJson = {
            'program_num': data[entry].program_num,
            'uncom_cert': data[entry].uncom_cert,
            'com_cert': data[entry].com_cert,
            'purpose_statement': data[entry].purpose_statement,
            
          }

          //console.log("body json: ", bodyJson)
        
          if (data[entry].app_num != ''){
            bodyJson['app_num'] = data[entry].app_num
            method = 'PUT'
          }

          //console.log('method: ', method)

          const res = await fetch(`https://csce-310-flask-backend-api.onrender.com/applications`, {
            method: method,
            headers: {
              'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(bodyJson)
          })
          //console.log('res', res)
        } catch (e) {
          console.error('errrrr', e)
        }

      }
  }


  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">

      <h1 className="text-3xl">Manage Users</h1>


      
      <div className="flex gap-3">

       

      <button
          onClick={addNewUser}
          className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded w-42'
        >Add new Application (+)</button>

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
        

      </div>
      <div className="ag-theme-quartz h-screen">
         <AgGridReact

          rowData={data}
          columnDefs={[
            {
              "field": "app_num",
              "headerName": "App Number",
     
            },
            {
              "field": "program_num",
              "headerName": "Program Number",
              "editable": editing
            },
            {
              "field": "uncom_cert",
              "headerName": "uncom cert",
              "editable": editing
              
            },
            {
              "field": "com_cert",
              "headerName": "com cert",
              "editable": editing
            },
            {
              "field": "purpose_statement",
              "headerName": "Purpose Statement",
              "editable": editing
            },
   
            {
              "headerName": "Delete Application",
              "cellRenderer": deleteButton, 
            },
   
          ]}
          
        /> 
      </div>
     
      
    </main>
  )
}
