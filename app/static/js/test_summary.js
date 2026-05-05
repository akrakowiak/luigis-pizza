function loadCart() {
    const cartData = localStorage.getItem('pizza_cart');
    return cartData ? JSON.parse(cartData) : [];
}

function updateCartUI() {
    const cart = loadCart();
    const cartItemsContainer = document.getElementById('cart-items-container');
    const cartSummary = document.getElementById('cart-summary');

    if (cart.length === 0) {
        cartItemsContainer.classList.add('empty');
        cartItemsContainer.innerHTML = `
            <i class="fa-solid fa-fire-burner text-4xl text-red-500"></i>
            <p class="mt-4 text-gray-600">Piec jest pusty. Dodaj pizzę z menu!</p>
        `;
        cartSummary.textContent = `Suma: 0.00 zł`;
        return;
    }

    cartItemsContainer.classList.remove('empty');
    cartItemsContainer.innerHTML = '';
    let total = 0;

    cart.forEach((item) => {
        const div = document.createElement('div');
        div.className = 'cart-item flex justify-between items-center mb-4';

        div.innerHTML = `
            <div class="text-left">
                <div class="text-xl font-bold">${item.pizzaName} (${item.sizeText.split('-')[0].trim()})</div>
                <div class="text-gray-600">${item.quantity} x ${item.sizeText.split('-')[1].trim()} zł</div>
            </div>
            <div class="text-lg font-semibold">${(item.quantity * parseFloat(item.sizeText.split('-')[1])).toFixed(2)} zł</div>
        `;

        cartItemsContainer.appendChild(div);
        total += item.quantity * parseFloat(item.sizeText.split('-')[1]);
    });

    cartSummary.textContent = `Suma: ${total.toFixed(2)} zł`;
}
document.addEventListener('DOMContentLoaded', updateCartUI);
