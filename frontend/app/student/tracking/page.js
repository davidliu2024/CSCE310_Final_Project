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
  const globalState = useUserStore();
  const [data, setData] = useState([]);
  const [tempData, setTempData] = useState([]);
  const [allPrograms, setAllPrograms] = useState([]);
  const [selectedProgram, setSelectedProgram] = useState('');
  const [selectedProgramDetails, setSelectedProgramDetails] = useState(null);
  const [signedUpPrograms, setSignedUpPrograms] = useState([]);
  const [signUpResponse, setSignUpResponse] = useState('');
  const [displaySignedUpPrograms, setDisplaySignedUpPrograms] = useState(false); // New state to control display

  // logistics state
  const [editing, setEditing] = useState(false);
  const [statusCode, setStatusCode] = useState('');
  const [areEmailsValid, setAreEmailsValid] = useState(true);

  const [allClasses, setAllClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedClassDetails, setSelectedClassDetails] = useState(null);

  const [enrolledPrograms, setEnrolledPrograms] = useState([]);
  const [enrolledClasses, setEnrolledClasses] = useState([]);
  const [internApps, setInternApps] = useState([]);
  const [certs, setCerts] = userState([])

  // get initial data including all programs
  useEffect(() => {
    const fetchPrograms = async () => {
      const programsResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const code = programsResponse.status;

      if (code === 200) {
        const json = await programsResponse.json();
        setAllPrograms(json);
      }
    };

    const fetchClasses = async () => {
      const classesResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const code = classesResponse.status;

      if (code === 200) {
        const json = await classesResponse.json();
        setAllClasses(json);
      }
    };

    fetchPrograms().catch(err => console.log(err, 'from the admin/users page'));
    fetchClasses().catch(err => console.log(err, 'from the admin/users page'));
  }, [globalState.username, globalState.password]);

  const fetchSignedUpPrograms = async () => {
    const signedUpProgramsResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs/user`, {
      method: 'GET',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
      }
    });

    const code = signedUpProgramsResponse.status;

    if (code === 200) {
      const json = await signedUpProgramsResponse.json();
      setSignedUpPrograms(json);
    }
  };

  const viewProgramDetails = async () => {
    if (!selectedProgram) {
      return;
    }

    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs/${selectedProgram}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
      }
    });

    const code = response.status;
    setStatusCode(code);

    if (code === 200) {
      const programDetails = await response.json();
      setSelectedProgramDetails(programDetails);
    }
  };

  // Function to remove user from the selected program
  const removeUserFromProgram = async () => {
    if (!selectedProgram) {
      return;
    }

    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs/${selectedProgram}/remove`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
      }
    });

    const code = response.status;
    setSignUpResponse(`Remove user response: ${code}`);
    fetchSignedUpPrograms(); // Refresh the signed-up programs list
  };

  const signUpForProgram = async () => {
    if (!selectedProgram) {
      return;
    }

    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs/${selectedProgram}/sign-up`, {
      method: 'PUT',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
      }
    });

    const code = response.status;
    setSignUpResponse(`Sign-up response: ${code}`);
    fetchSignedUpPrograms(); // Refresh the signed-up programs list
  };

  const addEnrollment = async () => {
    if (!selectedClass) {
      return;
    }

    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes/add-enrollment`, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        uin: 4,
        class_id: selectedClass,
        class_status: "Enrolled",
        semester: "SPRING",
        class_year: 2024
      }),
    });
    console.log(globalState.username, globalState.password)

    const code = response.status;
    setSignUpResponse(`Add enrollment response: ${code}`);
  };

  const removeEnrollment = async () => {
    if (!selectedClass) {
      return;
    }
    
    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes/remove-enrollment`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        class_id: selectedClass,
        uin: globalState.userUIN, 
      }),
    });

    const code = response.status;
    setSignUpResponse(`Remove enrollment response: ${code}`);
  };

  const viewClassDetails = async () => {
    if (!selectedClass) {
      return;
    }

    const response = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes/${selectedClass}`, {
      method: 'GET',
      headers: {
        'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
      }
    });

    const code = response.status;
    setStatusCode(code);

    if (code === 200) {
      const classDetails = await response.json();
      setSelectedClassDetails(classDetails);
    }
  };

  const fetchEnrolledPrograms = async () => {
    try {
      const enrolledProgramsResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/programs/user`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const enrolledProgramsCode = enrolledProgramsResponse.status;

      if (enrolledProgramsCode === 200) {
        const enrolledProgramsJson = await enrolledProgramsResponse.json();
        setEnrolledPrograms(enrolledProgramsJson);
      }
    } catch (error) {
      console.error('Error fetching enrolled programs:', error);
    }
  };

  const fetchEnrolledClasses = async () => {
    try {
      const enrolledClassesResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes/fetch-enrollments`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const enrolledClassesCode = enrolledClassesResponse.status;

      if (enrolledClassesCode === 200) {
        const enrolledClassesJson = await enrolledClassesResponse.json();
        setEnrolledClasses(enrolledClassesJson);
      }
    } catch (error) {
      console.error('Error fetching enrolled classes:', error);
    }
  };

  const fetchInternApps = async () => {
    try {
      const enrolledClassesResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/intern-apps`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const enrolledClassesCode = enrolledClassesResponse.status;

      if (enrolledClassesCode === 200) {
        const enrolledClassesJson = await enrolledClassesResponse.json();
        setInternApps(enrolledClassesJson);
      }
    } catch (error) {
      console.error('Error fetching enrolled classes:', error);
    }
  };

  const fetchCerts = async () => {
    try {
      const enrolledClassesResponse = await fetch(`https://csce-310-flask-backend-api.onrender.com/classes/fetch-enrollments`, {
        method: 'GET',
        headers: {
          'Authorization': 'Basic ' + Buffer.from(globalState.username + ":" + globalState.password).toString('base64')
        }
      });

      const enrolledClassesCode = enrolledClassesResponse.status;

      if (enrolledClassesCode === 200) {
        const enrolledClassesJson = await enrolledClassesResponse.json();
        setCerts(enrolledClassesJson);
      }
    } catch (error) {
      console.error('Error fetching enrolled classes:', error);
    }
  };

  const displayEnrolledProgramsHandler = async () => {
    try {
      // Fetch enrolled programs
      await fetchEnrolledPrograms();

      // Fetch enrolled classes
      await fetchEnrolledClasses();
    } catch (error) {
      console.error('Error fetching enrolled programs and classes:', error);
    }

    setDisplaySignedUpPrograms(!displaySignedUpPrograms);
  };


  return (
    <main className="h-screen flex flex-col px-5 py-3 gap-5">
      <h1 className="text-3xl">Manage Users</h1>

      <div className="flex gap-3">
        <button
          onClick={viewProgramDetails}
          disabled={!selectedProgram}
          className='bg-yellow-500 hover:bg-yellow-400 text-white font-bold py-2 px-4 border-b-4 border-yellow-700 hover:border-yellow-500 rounded w-42'
        >
          View Program Details
        </button>

        <button
          onClick={signUpForProgram}
          disabled={!selectedProgram}
          className='bg-green-500 hover:bg-green-400 text-white font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded w-42'
        >
          Sign Up For Program
        </button>

        {/* Remove User from Program button */}
        <button
          onClick={removeUserFromProgram}
          disabled={!selectedProgram}
          className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded w-42'
        >
          Remove User from Program
        </button>

        {!areEmailsValid ?
          <span className="text-sm text-red-600">Ensure no emails are empty & all are valid</span> : ''
        }
      </div>

      <div>
        <label htmlFor="allProgramsDropdown" className="text-sm">Select Program:</label>
        <select
          id="allProgramsDropdown"
          value={selectedProgram}
          onChange={(e) => setSelectedProgram(e.target.value)}
          className="bg-white border border-gray-300 p-2 rounded-md"
        >
          <option value="" disabled>Select a Program</option>
          {allPrograms.map(program => (
            <option key={program.program_num} value={program.program_num}>
              {program.program_name}
            </option>
          ))}
        </select>
      </div>

      <div className="flex gap-3">
       <button
          onClick={viewClassDetails}
          disabled={!selectedClass}
          className='bg-yellow-500 hover:bg-yellow-400 text-white font-bold py-2 px-4 border-b-4 border-yellow-700 hover:border-yellow-500 rounded w-42'
        >
          View Class Details
        </button>

        <button
          onClick={addEnrollment}
          disabled={!selectedClass}
          className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded w-42'
        >
          Add Enrollment
        </button>

        <button
          onClick={removeEnrollment}
          disabled={!selectedClass}
          className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded w-42'
        >
          Remove Enrollment
        </button>

      </div>

      <div>
        <label htmlFor="allClassesDropdown" className="text-sm">Select Class:</label>
        <select
          id="allClassesDropdown"
          value={selectedClass}
          onChange={(e) => setSelectedClass(e.target.value)}
          className="bg-white border border-gray-300 p-2 rounded-md"
        >
          <option value="" disabled>Select a Class</option>
          {allClasses.map(classItem => (
            <option key={classItem.class_id} value={classItem.class_id}>
              {classItem.class_name}
            </option>
          ))}
        </select>
      </div>
      

      {selectedProgramDetails && (
        <div className="mt-5">
          <h2 className="text-xl font-semibold">Program Details</h2>
          <pre>{JSON.stringify(selectedProgramDetails, null, 2)}</pre>
        </div>
      )}

      {selectedClassDetails && (
        <div className="mt-5">
          <h2 className="text-xl font-semibold">Class Details</h2>
          <pre>{JSON.stringify(selectedClassDetails, null, 2)}</pre>
        </div>
      )}

      <button
        onClick={displayEnrolledProgramsHandler}
        className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded mt-5 w-42'
      >
        Display Enrolled Programs and Classes
      </button>

      {displaySignedUpPrograms && (
        <div className="mt-5">
          <h2 className="text-xl font-semibold">Enrolled Programs</h2>
          <ul>
            {enrolledPrograms.map(program => (
              <li key={program.program_num}>{program.program_name}</li>
            ))}
          </ul>

          <h2 className="text-xl font-semibold mt-5">Enrolled Classes</h2>
          <ul>
            {enrolledClasses.map(classItem => (
              <li key={classItem.ce_num*classItem.class_id}>{classItem.class_details.class_name}</li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
