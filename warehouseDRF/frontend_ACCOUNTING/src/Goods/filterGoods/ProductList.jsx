// components/ProductList.js
import React from 'react';

const ProductList = ({ products }) => {
  if (products.length === 0) {
    return <div className="no-products">Товары не найдены</div>;
  }

  return (
    <div className="product-list">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          {product.description && <p>{product.description}</p>}
          <p className="price">Цена: {product.price} ₽</p>
        </div>
      ))}
    </div>
  );
};

export default ProductList;