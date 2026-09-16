import styles from './ProductCard.module.css'

const formatPrice = (price, currency) => price === null || price === undefined
  ? 'Price unavailable'
  : `${new Intl.NumberFormat('hu-HU').format(price)} ${currency}`

function ProductCard({ product, type, onSelect }) {
  const specs = type === 'laptops'
    ? [product.brand, product.model]
    : [product.brand, product.model, product.vram_gb && `${product.vram_gb} GB VRAM`]

  return (
    <article className={styles.card}>
      <button className={styles.cardButton} onClick={() => onSelect(product)} aria-label={`View ${product.title}`}>
        <div className={styles.imageWrap}>
          {product.img_url ? <img src={product.img_url} alt="" /> : <span className={styles.imageFallback}>{type === 'laptops' ? 'LAPTOP' : 'GPU'}</span>}
          {product.iced_status && <span className={styles.badge}>ICED</span>}
          {product.archived_at && <span className={styles.archivedBadge}>ARCHIVED</span>}
        </div>
        <div className={styles.cardBody}><div className={styles.cardTopline}><span>{product.brand || product.site}</span><span>{product.location || 'Location unknown'}</span></div><h3>{product.title}</h3><p className={styles.price}>{formatPrice(product.price, product.currency)}</p><div className={styles.specs}>{specs.filter(Boolean).map((spec) => <span key={spec}>{spec}</span>)}</div></div>
      </button>
      <div className={styles.cardFooter}><span>{product.site}</span><span>View details →</span></div>
    </article>
  )
}

export default ProductCard