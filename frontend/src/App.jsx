import { useEffect, useRef, useState } from 'react'
import { fetchListingDetail, fetchListings } from './api'
import ProductCard from './ProductCard'

const PAGE_SIZE = 24
const initialFilters = { title: '', site: '', brand: '', model: '', min_price: '', max_price: '', cpu_brand: '', gpu_brand: '', min_ram_gb: '', min_storage_size_gb: '', min_vram_gb: '', max_vram_gb: '', location: '', iced_status: false, include_archived: false }

function App() {
  const [type, setType] = useState('laptops')
  const [draftFilters, setDraftFilters] = useState(initialFilters)
  const [filters, setFilters] = useState(initialFilters)
  const [listings, setListings] = useState([])
  const [skip, setSkip] = useState(0)
  const [hasMore, setHasMore] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)
  const [detail, setDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState('')
  const sentinelRef = useRef(null)
  const requestInFlightRef = useRef(false)

  const updateFilter = (event) => {
    const { name, value, checked, type: inputType } = event.target
    setDraftFilters((current) => ({ ...current, [name]: inputType === 'checkbox' ? checked : value }))
  }

  const loadPage = async (offset, replace = false) => {
    if (requestInFlightRef.current || (!hasMore && !replace)) return
    requestInFlightRef.current = true
    setLoading(true)
    setError('')
    try {
      const page = await fetchListings(type, filters, offset, PAGE_SIZE)
      setListings((current) => (replace ? page : [...current, ...page]))
      setSkip(offset + page.length)
      setHasMore(page.length === PAGE_SIZE)
    } catch (requestError) { setError(requestError.message) } finally {
      requestInFlightRef.current = false
      setLoading(false)
    }
  }

  useEffect(() => {
    setListings([]); setSkip(0); setHasMore(true); loadPage(0, true)
  }, [type, filters])

  useEffect(() => {
    const node = sentinelRef.current
    if (!node) return undefined
    const observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) loadPage(skip) }, { rootMargin: '480px' })
    observer.observe(node)
    return () => observer.disconnect()
  }, [skip, hasMore, loading, type, filters])

  const submitFilters = (event) => { event.preventDefault(); setFilters({ ...draftFilters }) }
  const changeType = (nextType) => { setType(nextType); setSelected(null); setDetail(null) }
  const closeDetail = () => { setSelected(null); setDetail(null) }

  const openDetail = async (listing) => {
    setSelected(listing); setDetail(null); setDetailError(''); setDetailLoading(true)
    try { setDetail(await fetchListingDetail(type, listing.site, listing.listing_id)) } catch (requestError) { setDetailError(requestError.message) } finally { setDetailLoading(false) }
  }

  return (
    <main className="app-shell">
      <header className="masthead"><div><p className="eyebrow">LOCAL LISTING INDEX</p><h1>Find the right machine.</h1><p className="intro">Search enriched marketplace listings by the specs that matter.</p></div><div className="type-switch" aria-label="Product type"><button className={type === 'laptops' ? 'active' : ''} onClick={() => changeType('laptops')}>Laptops</button><button className={type === 'gpus' ? 'active' : ''} onClick={() => changeType('gpus')}>GPUs</button></div></header>
      <section className="workspace">
        <form className="filter-panel" onSubmit={submitFilters}><div className="filter-heading"><div><span className="section-kicker">FILTERS</span><h2>Refine results</h2></div><button className="clear-button" type="button" onClick={() => { setDraftFilters(initialFilters); setFilters(initialFilters) }}>Clear all</button></div><label className="search-field">Search title<input name="title" value={draftFilters.title} onChange={updateFilter} placeholder="ThinkPad, RTX 3080..." /></label><div className="field-grid two-columns"><label>Brand<input name="brand" value={draftFilters.brand} onChange={updateFilter} placeholder="Lenovo" /></label><label>Model<input name="model" value={draftFilters.model} onChange={updateFilter} placeholder="Legion 5" /></label><label>Min price<input name="min_price" type="number" min="0" value={draftFilters.min_price} onChange={updateFilter} placeholder="HUF" /></label><label>Max price<input name="max_price" type="number" min="0" value={draftFilters.max_price} onChange={updateFilter} placeholder="HUF" /></label></div>{type === 'laptops' ? <div className="field-grid two-columns"><label>CPU brand<input name="cpu_brand" value={draftFilters.cpu_brand} onChange={updateFilter} placeholder="Intel" /></label><label>GPU brand<input name="gpu_brand" value={draftFilters.gpu_brand} onChange={updateFilter} placeholder="NVIDIA" /></label><label>Min RAM (GB)<input name="min_ram_gb" type="number" min="0" value={draftFilters.min_ram_gb} onChange={updateFilter} /></label><label>Min storage (GB)<input name="min_storage_size_gb" type="number" min="0" value={draftFilters.min_storage_size_gb} onChange={updateFilter} /></label></div> : <div className="field-grid two-columns"><label>Min VRAM (GB)<input name="min_vram_gb" type="number" min="0" value={draftFilters.min_vram_gb} onChange={updateFilter} /></label><label>Max VRAM (GB)<input name="max_vram_gb" type="number" min="0" value={draftFilters.max_vram_gb} onChange={updateFilter} /></label></div>}<label>Location<input name="location" value={draftFilters.location} onChange={updateFilter} placeholder="Budapest" /></label><div className="check-list"><label><input name="iced_status" type="checkbox" checked={draftFilters.iced_status} onChange={updateFilter} /> Include iced listings</label><label><input name="include_archived" type="checkbox" checked={draftFilters.include_archived} onChange={updateFilter} /> Include archived listings</label></div><button className="apply-button" type="submit">Apply filters <span>→</span></button></form>
        <section className="results-panel" aria-live="polite"><div className="results-heading"><div><span className="section-kicker">{type === 'laptops' ? 'ENRICHED LAPTOPS' : 'ENRICHED GPUS'}</span><h2>{listings.length ? `${listings.length} listings loaded` : 'Browse listings'}</h2></div><span className="status-dot">{loading ? 'Updating' : 'Live index'}</span></div>{error && <div className="message error-message"><strong>Could not load listings.</strong><span>{error}</span><button onClick={() => loadPage(skip, listings.length === 0)}>Retry</button></div>}{!error && !loading && listings.length === 0 && <div className="message empty-message"><strong>No matches yet.</strong><span>Try widening your filters or switching product type.</span></div>}<div className="listing-grid">{listings.map((listing) => <ProductCard key={`${listing.site}-${listing.listing_id}`} product={listing} type={type} onSelect={openDetail} />)}</div><div ref={sentinelRef} className="scroll-status">{loading && <span className="loader">Loading more listings...</span>}{!loading && !hasMore && listings.length > 0 && <span>You've reached the end of the index.</span>}{!loading && hasMore && listings.length > 0 && <button className="load-button" onClick={() => loadPage(skip)}>Load more</button>}</div></section>
      </section>
      {selected && <div className="detail-page"><div className="detail-page-content"><button className="back-button" onClick={closeDetail}>← Back to results</button>{detailLoading && <div className="drawer-state">Loading details...</div>}{detailError && <div className="drawer-state error-message"><strong>{detailError}</strong></div>}{detail && <><div className="drawer-image">{detail.img_url ? <img src={detail.img_url} alt="" /> : <span>{type === 'laptops' ? 'LAPTOP' : 'GPU'}</span>}</div><span className="section-kicker">{detail.brand || 'Unknown brand'} · {detail.site}</span><h2>{detail.title}</h2><p className="detail-price">{detail.price ? `${new Intl.NumberFormat('hu-HU').format(detail.price)} ${detail.currency}` : 'Price unavailable'}</p><div className="spec-list">{Object.entries(detail).filter(([key, value]) => value !== null && value !== '' && !['title', 'price', 'currency', 'img_url', 'description'].includes(key)).slice(0, 14).map(([key, value]) => <div key={key}><span>{key.replaceAll('_', ' ')}</span><strong>{String(value)}</strong></div>)}</div>{detail.description && <p className="description">{detail.description}</p>}<a className="source-link" href={detail.listing_url} target="_blank" rel="noreferrer">Open original listing ↗</a></>}</div></div>}
    </main>
  )
}

export default App
