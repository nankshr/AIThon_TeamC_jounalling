import Link from 'next/link'
import { Heart } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Heart className="w-8 h-8 text-pink-500 fill-pink-500" />
            <h1 className="text-3xl font-bold text-gray-900">Wedding Journal</h1>
          </div>

          <nav className="flex items-center gap-6">
            <Link
              href="/"
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              Journal
            </Link>
            <Link
              href="/search"
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              Search
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}
