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
  const [allDocuments, setAllDocuments] = useState([])
  const [editing, setEditing] = useState(false)
  const [file, setfile] = useState()

  // logistics state

  const [statusCode, setStatusCode] = useState('')


  // get initial data

  const deleteButton = (props) => {
    const deleteReq = async () => {
      console.log(props.route.doc_id)
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/${props.route.doc_id}/document}`, {
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

        setAllDocuments(json)
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
  useEffect(() => {
    const fetchUsers = async () => {
   
      const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/applications/documents/user`, {
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

        setAllDocuments(json)
      }

    }

    fetchUsers()
      .catch(err => console.log(err, 'from the student/documents page'))
  }, [])


  const saveData = async () => {



    if (file) {
      try {
        const fileData = new FormData()
        fileData.set('file', file)
       
        console.log(fileData)
        
        const res = await fetch(`https://csce-310-flask-backend-api.onrender.com/applications/documents/4`, {
          method: 'POST',
          headers: {
            'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64'),
          },
          body: fileData
        })
       
     
        if (!res.ok) throw new Error(await res.json())
      } catch (e) {
        console.error(e)
      }

    }

 
  }


  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">
      <h1 class="text-3xl">Documents</h1>

      
      <div className="flex gap-3">

            <form >
              <input
                type="file"
                name="file"
                onChange={(e) => setfile(e.target.files?.[0])}//
                
              />
            </form>


            <button
              onClick={saveData}
              className='bg-green-500 hover:bg-green-400 text-white font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded w-42'
            >Submit Document</button>
        

      </div>
      <div className="ag-theme-quartz h-screen">
         <AgGridReact

          rowData={allDocuments}
          columnDefs={[
            {
              "field": "program_name",
              "headerName": "App Number",
              
            },
            {
              "field": "doc_link",
              "headerName": "Link",
              "editable":true
            },
            {
              "headerName": "Delete",
              "cellRenderer": deleteButton,
              "cellRendereParams": {
                "doc_id": 12
              }
            }
           
          ]}
          
        /> 
      </div>
     
      
    </main>
  )
}
