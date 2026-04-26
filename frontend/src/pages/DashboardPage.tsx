import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { setAuthToken, getCurrentUser, getSearches } from '../api/client'
import type { User, SearchHistoryItem } from '../types'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [user, setUser] = useState<User | null>(null)
  const [searches, setSearches] = useState<SearchHistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    async function loadData() {
      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
        const searchesData = await getSearches()
        setSearches(searchesData)
      } catch {
        setAuthToken(null)
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [navigate, refreshKey])

  function handleLogout() {
    setAuthToken(null)
    navigate('/login')
  }

  function handleRefresh() {
    setRefreshKey((k) => k + 1)
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h2>PII Scanner</h2>
        <div className="nav-user">
          <span>{user?.email}</span>
          <button onClick={handleRefresh}>Refresh</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="card scan-card">
          <h3>Scan Your Data</h3>
          <p>Find where your personal information appears online.</p>
          <Link to="/scan" className="btn btn-primary">Start New Scan</Link>
        </div>

        <div className="card history-card">
          <h3>Recent Searches</h3>
          {searches.length === 0 ? (
            <p className="empty">No searches yet. Start your first scan!</p>
          ) : (
            <ul className="search-list">
              {searches.map((search) => (
                <li key={search.id}>
                  <Link to={`/results/${search.id}`}>
                    <span className="search-name">
                      {search.first_name} {search.last_name}
                    </span>
                    <span className="search-date">
                      {new Date(search.created_at).toLocaleDateString()}{' '}
                      {new Date(search.created_at).toLocaleTimeString()}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}