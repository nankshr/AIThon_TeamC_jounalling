import type { Metadata } from 'next'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Wedding Journal',
  description: 'AI-powered wedding planning journal',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-slate-50 to-slate-100">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
