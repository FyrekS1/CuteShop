let allProducts = [];

async function findWorkingImageUrl(art) {
  art = String(art);
  const vol = art.length === 9 ? art.slice(0, 4) : art.slice(0, 3);
  const part = art.length === 9 ? art.slice(0, 6) : art.slice(0, 5);

  for (let i = 1; i <= 30; i++) {
    const server = i.toString().padStart(2, '0');
    const url = `https://basket-${server}.wbbasket.ru/vol${vol}/part${part}/${art}/images/big/1.webp`;

    try {
      const response = await fetch(url, { method: 'HEAD' });
      if (response.ok) return url;
    } catch (e) {}
  }

  return 'https://via.placeholder.com/300x200?text=Нет+фото';
}

async function loadProducts() {
  const response = await fetch('products1.json');
  allProducts = await response.json();
  await renderProducts(allProducts);

  // Скрываем лоадер плавно
  const loader = document.getElementById('loader');
  loader.classList.add('hidden');

  // Через 2 секунды показываем заголовок (1.5 сек)
  setTimeout(() => {
    const catalog = document.getElementById('catalog');
    catalog.classList.remove('hidden-opacity');
    catalog.classList.add('visible-opacity');

    // Через 1.5 секунды показываем поиск (1 сек)
    setTimeout(() => {
      const searchCss = document.getElementById('search-css');
      searchCss.classList.remove('hidden-opacity');
      searchCss.classList.add('visible-opacity');

      // Через 1 секунду показываем список товаров (1.5 сек)
      setTimeout(() => {
        const productList = document.getElementById('product-list');
        productList.classList.remove('hidden-opacity');
        productList.classList.add('visible-opacity');
      }, 1000);
    }, 1500);
  }, 2000);
}

async function renderProducts(productArray) {
  const container = document.getElementById('product-list');
  container.innerHTML = '';

  const cardsData = await Promise.all(
    productArray.map(async (product) => {
      const art = product['Артикул WB'];
      const imageUrl = await findWorkingImageUrl(art);
      return { product, imageUrl };
    })
  );

  for (const { product, imageUrl } of cardsData) {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${imageUrl}" alt="${product['Наименование']}">
      <h2>${product['Наименование']}</h2>
      <p>${product['Текущая цена']} ₽ <strong style="color:red">${product['Цена со скидкой']} ₽</strong></p>
    `;
    container.appendChild(card);
  }
}

function search() {
  const query = document.getElementById('site-search').value.trim().toLowerCase();
  const filtered = allProducts.filter((product) =>
    product['Наименование'].toLowerCase().includes(query)
  );
  renderProducts(filtered);
}

// Изначально скрываем элементы
document.getElementById('catalog').classList.add('hidden-opacity');
document.getElementById('search-css').classList.add('hidden-opacity');
document.getElementById('product-list').classList.add('hidden-opacity');

loadProducts();
