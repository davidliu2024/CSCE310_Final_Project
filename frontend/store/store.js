import { create } from 'zustand'

const useUserStore = create((set) => ({
    username: '',
    password: '',
    authToken: '',
    details: {},
    setDetails: (_details) => set((state) => ({ details: _details})),
    setUsername: (_username) => set((state) => ({ username: _username})),
    setPassword: (_password) => set((state) => ({ password: _password})),
    setAuthToken: (token) => set((state) => ({ authToken: token }))
}))

export { useUserStore }