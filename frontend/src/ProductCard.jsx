import React from 'react';
// Import the CSS module. Note the `styles` import name.
import styles from './ProductCard.module.css';

const ProductCardCSS = ({ product }) => {
  const { title, price, iced_status, image_url, seller, location, list_date } = product;

  const formattedPrice = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price);
  const formattedDate = new Date(list_date).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });

  return (
    <div className={styles.cardContainer}>
      {/* --- Image Section --- */}
      <div className={styles.imageWrapper}>
        <img src={image_url} alt={title} className={styles.productImage} />
        {iced_status && (
          <div className={styles.icedBadge}>
             ❄️ ICED
          </div>
        )}
      </div>

      {/* --- Content Body --- */}
      <div className={styles.cardBody}>
        <h3 className={styles.title} title={title}>{title}</h3>
        <p className={styles.price}>{formattedPrice}</p>

        <div className={styles.sellerSection}>
          <span className={styles.sellerName}>{seller.name}</span>
          <span className={styles.rating}>★ {seller.rating}</span>
        </div>
      </div>

      {/* --- Footer --- */}
      <div className={styles.cardFooter}>
        <span className={styles.metaItem}>📍 {location}</span>
        <span className={styles.metaItem}>📅 {formattedDate}</span>
      </div>
    </div>
  );
};

export default ProductCardCSS;