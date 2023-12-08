"use client"

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Inter } from 'next/font/google'
import './globals.css'

import { useUserStore } from '@/store/store'

export default function RootLayout({ children }) {
  const authToken = useUserStore(state => state.authToken)
  const router = useRouter();

  useEffect(() => {
    if (!authToken && !["/", "/signup", "/resetpass"].includes(router.pathname)) {
      router.push("/"); // TODO: make a loading screen so no FOUC
    }
    else if (authToken === 'user' && !router.pathname.includes('user')) {
      router.push("/student/")
    }
    else if (authToken === 'admin' && !router.pathname.includes('admin')) {
      router.push("/admin/")
    }
  }, []);

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
