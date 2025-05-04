// utils/filterProducts.js
//Логика фильтрации товаров
export const filterProducts = (products, searchTerm) => {
  if (!searchTerm) return products;
  
  const lowercasedSearch = searchTerm.toLowerCase();
  
  return products.filter(product => 
    product.name.toLowerCase().includes(lowercasedSearch) ||
    (product.description && product.description.toLowerCase().includes(lowercasedSearch)) ||
    (product.category && product.category.name.toLowerCase().includes(lowercasedSearch))
  );
};