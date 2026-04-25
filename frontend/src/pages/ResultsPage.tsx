import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getSearchResult } from '../api/client'
import type { SearchResult } from '../types'

export default function ResultsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [result, setResult] = useState<SearchResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadResult() {
      if (!id) return
      try {
        const data = await getSearchResult(parseInt(id))
        setResult(data)
      } catch {
        setError('Failed to load results')
      } finally {
        setLoading(false)
      }
    }
    loadResult()
  }, [id])

  if (loading) {
    return <div className="loading">Loading results...</div>
  }

  if (error || !result) {
    return (
      <div className="results-page">
        <nav className="navbar">
          <Link to="/dashboard">Back to Dashboard</Link>
        </nav>
        <div className="error">{error || 'Results not found'}</div>
      </div>
    )
  }

  const dataFoundCount = result.sources.filter((s) => s.data_found).length
  const totalSources = result.sources.length

  return (
    <div className="results-page">
      <nav className="navbar">
        <button onClick={() => navigate('/dashboard')} className="btn-back">
          Back to Dashboard
        </button>
      </nav>

      <div className="results-container">
        <div className="results-header">
          <h1>
            Results for {result.first_name} {result.last_name}
          </h1>
          <p className="scan-date">
            Scanned on {new Date(result.created_at).toLocaleDateString()}
          </p>
        </div>

        <div className="summary-card">
          <h3>Summary</h3>
          <div className="summary-stats">
            <div className="stat">
              <span className="stat-value">{totalSources}</span>
              <span className="stat-label">Sources Checked</span>
            </div>
            <div className="stat">
              <span className="stat-value">{dataFoundCount}</span>
              <span className="stat-label">Data Found In</span>
            </div>
          </div>
        </div>

        <div className="results-section">
          <h3>Searched Information</h3>
          <div className="info-grid">
            {result.email && (
              <div className="info-item">
                <span className="info-label">Email</span>
                <span className="info-value">{result.email}</span>
              </div>
            )}
            {result.phone && (
              <div className="info-item">
                <span className="info-label">Phone</span>
                <span className="info-value">{result.phone}</span>
              </div>
            )}
            {result.address && (
              <div className="info-item">
                <span className="info-label">Address</span>
                <span className="info-value">
                  {result.address}
                  {result.city && `, ${result.city}`}
                  {result.state && ` ${result.state}`}
                </span>
              </div>
            )}
          </div>
        </div>

        {result.sources.length > 0 ? (
          <div className="results-section">
            <h3>Data Sources</h3>
            <ul className="sources-list">
              {result.sources.map((source, index) => (
                <li key={index} className={source.data_found ? 'found' : 'not-found'}>
                  <div className="source-header">
                    <span className="source-name">{source.source_name}</span>
                    {source.data_found && (
                      <span className="badge badge-danger">Data Found</span>
                    )}
                  </div>
                  {source.source_url && (
                    <a
                      href={source.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="source-link"
                    >
                      Visit Source
                    </a>
                  )}
                  {source.data_details && (
                    <p className="source-details">{source.data_details}</p>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="results-section">
            <p className="empty-results">
              No data sources have been checked yet. Integration coming soon.
            </p>
          </div>
        )}

        <div className="results-actions">
          <Link to="/scan" className="btn btn-primary">
            Start New Scan
          </Link>
        </div>
      </div>
    </div>
  )
}