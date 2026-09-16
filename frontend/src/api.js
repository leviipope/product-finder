const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const endpointFor = (type) => `${API_BASE_URL}/listings/${type}`

const appendFilter = (params, key, value) => {
  if (value !== '' && value !== null && value !== undefined) {
    params.set(key, String(value))
  }
}

export async function fetchListings(type, filters, skip, limit) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })

  Object.entries(filters).forEach(([key, value]) => appendFilter(params, key, value))

  const response = await fetch(`${endpointFor(type)}?${params}`)
  if (!response.ok) {
    throw new Error(`Could not load listings (${response.status})`)
  }

  return response.json()
}

export async function fetchListingDetail(type, site, listingId) {
  const response = await fetch(`${endpointFor(type)}/${encodeURIComponent(site)}/${listingId}`)
  if (!response.ok) {
    throw new Error(`Could not load listing details (${response.status})`)
  }

  return response.json()
}
