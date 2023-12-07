'use client'

export default function Home() {

  return (
    <main className="h-screen flex flex-col">
      <h1 class="text-3xl m-3">Manage Users</h1>

      <button 
            className='bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded w-96'
      >Add new user+</button>
    </main>
  )
}
