// components/ProductList.js
import React from 'react';

const GoodsList = ({ goods }) => {
  if (goods.length === 0) {
    return <div className="no-products">Товары не найдены</div>;
  }

  return (
    <div className="product-list">
      {goods.map(product => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          {product.description && <p className="description">{product.description}</p>}
          <p className="price">Цена: {product.price} ₽</p>
        </div>
      ))}
    </div>


              {goods?.map(good => (
                        <div className="goods" key={good.id}>                         
                          <h3>{good.name_product}</h3>
                          <h4>Цена: {good.price}</h4>
                          <h4>Остаток: {good.stock}</h4>
                          <button onClick={() => modifyGood(good.id)}>Редактировать</button>
                          &nbsp;&nbsp;
                          <button onClick={() => deleteGood(good.id)}>Удалить</button>
                          {/*<Button onClick={() => Add_in_basket(good.id)}>Добавить в корзину</Button>*/}
                          {/*<p>{error}</p>*/}
                        </div>
                    ))}

  );
};

export default ProductList;