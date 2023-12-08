'use client'

import { UserIcon, CalendarIcon, PresentationChartLineIcon, GlobeAsiaAustraliaIcon } from '@heroicons/react/24/outline'
import { useUserStore } from '@/store/store';
import Link from 'next/link'
import { useRouter } from 'next/navigation';

const DashboardLayout = ({ children }) => {
  const globalState = useUserStore()
  const router = useRouter()

  const logout_func = (req, res) => {
    globalState.setUsername('')
    globalState.setPassword('')
    globalState.setAuthToken('')
    router.push('/')
  }

  return (
    <div className="flex">
      <aside className="flex-[2] min-w-[200px] w-full flex flex-col justify-between">
        <ul>
          <Link href="/admin/users">    <li className="py-5 px-4 flex gap-2 hover:bg-slate-100"><UserIcon width={24} /><span>Users</span></li></Link>
          <Link href="/admin/programs"> <li className="py-5 px-4 flex gap-2 hover:bg-slate-100"><GlobeAsiaAustraliaIcon width={24} /><span>Programs</span></li></Link>
          <Link href="/admin/tracking"> <li className="py-5 px-4 flex gap-2 hover:bg-slate-100"><PresentationChartLineIcon width={24} /><span>Tracking</span></li></Link>
          <Link href="/admin/events"><li className="py-5 px-4 flex gap-2 hover:bg-slate-100"><CalendarIcon width={24} /><span>Events</span></li></Link>
        </ul>
        
        <button
          className='bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded w-11/12 self-center my-5'
          onClick={logout_func}
        >Logout</button>

      </aside>
      <div className="bg-gray-100 flex-[8] rounded min-h-[300px]">
        {children}
      </div>
    </div>
  );
};

export default DashboardLayout;