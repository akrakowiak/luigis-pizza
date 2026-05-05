let cart = [];
const origin = window.location.origin;
const pizzaTemplate = document.querySelector("#pizza-template");
const cartItemsContainer = document.querySelector("#cart-items-container")
const cartSummary = document.querySelector("#cart-summary")

const sizeNameToSize = {
    "small": 1,
    "medium": 2,
    "large": 3
}

const sizeToSizeName = {
    1: "small",
    2: "medium",
    3: "large"
}

const getSizeName = (pizza) => ({
    1: "Mała",
    2: "Średnia",
    3: "Duża"
}[pizza.size]);

const getPrice = (pizza) => pizza[`${sizeToSizeName[pizza.size]}_price`];

const responseCartToCart = (cart) => {
    const cartGrouped = {}

    for (const pizza of cart) {
        const idSize = `${pizza.id}-${pizza.size}`;

        if (idSize in cartGrouped) {
            cartGrouped[idSize].quantity += 1;
        } else {
            cartGrouped[idSize] = {
                ...pizza,
                quantity: 1
            };
        }
    }

    return Object.values(cartGrouped).sort((a, b) => a.id.localeCompare(b.id));
}

async function addToCart(e) {
    const pizzaElement = e.target.closest("*[data-pizza-id]");
    const sizeElement = pizzaElement.getElementsByClassName("pizza-size")[0];

    const { pizzaId, pizzaName } = pizzaElement.dataset;
    const size = sizeElement.value;
    const sizeText = sizeElement.selectedOptions[0].textContent;

    const response = await fetch(origin + "/api/cart", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "pizza_id": pizzaId,
            "pizza_size": sizeNameToSize[size]
        })
    })
    const json = await response.json()

    if (!response.ok) {
        console.error(response, json)
    }

    cart = responseCartToCart(json);

    updateCartUI();
}

async function increasePizzaQuantity(event) {
    const cartItem = event.target.closest(".cart-item");
    const {pizzaId, pizzaSize} = cartItem.dataset;

    const response = await fetch(origin + "/api/cart", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "pizza_id": pizzaId,
            "pizza_size": +pizzaSize
        })
    })

    if (!response.ok) {
        const json = await response.json();
        console.error(response, json);
    }

    const cartItemQuantity = cartItem.querySelector(".cart-item-quantity")
    cartItemQuantity.textContent = +cartItemQuantity.textContent + 1
}

async function decreasePizzaQuantity(event) {
    const cartItem = event.target.closest(".cart-item");
    const {pizzaId, pizzaSize} = cartItem.dataset;

    const success = removeFromCartRequest(pizzaId, pizzaSize);

    const cartItemQuantity = cartItem.querySelector(".cart-item-quantity")
    cartItemQuantity.textContent = +cartItemQuantity.textContent - 1
}

async function clearPizzas(event) {
    const cartItem = event.target.closest(".cart-item");
    const {pizzaId, pizzaSize} = cartItem.dataset;

    let success = true;
    while (success) {
        const success = removeFromCartRequest(pizzaId, pizzaSize);
    }

    cartItem.remove();
}

async function removeFromCartRequest(pizzaId, pizzaSize) {
    const response = await fetch(origin + "/api/cart", {
        method: "DELETE",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "pizza_id": pizzaId,
            "pizza_size": +pizzaSize
        })
    })

    if (!response.ok) {
        const json = await response.json();
        console.error(response, json);
        return false;
    }

    return true;
}

async function removeFromCart(e) {
    const response = await fetch(origin + "/api/cart", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "pizza_id": pizzaId,
            "pizza_size": sizeNameToSize[size]
        })
    })

    if (!response.ok) {
        console.error(response, json)
    }

    cart.splice(index, 1);
    updateCartUI();
}

function cartItemToElement(cartItem) {
    const cartItemElement = pizzaTemplate.content.cloneNode(true);

    const cartItemName = `${cartItem.name} (${getSizeName(cartItem)})`;
    const cartItemPrice = `${(getPrice(cartItem) * cartItem.quantity).toFixed(2)} zł`
    const cartItemQuantity = cartItem.quantity

    cartItemElement.children[0].dataset.pizzaId = cartItem.id;
    cartItemElement.children[0].dataset.pizzaSize = cartItem.size;
    cartItemElement.querySelector(".cart-item-name").textContent = cartItemName;
    cartItemElement.querySelector(".cart-item-price").textContent = cartItemPrice;
    cartItemElement.querySelector(".cart-item-quantity").textContent = cartItemQuantity;

    return cartItemElement;
}

function updateCartUI() {
    if (cart.length === 0) {
        cartItemsContainer.classList.add("empty");
        return;
    }

    cartItemsContainer.classList.remove("empty");
    cartItemsContainer.innerHTML = "";

    let total = 0;

    cart.forEach((cartItem, index) => {
        cartItemsContainer.appendChild(cartItemToElement(cartItem));
        total += getPrice(cartItem) * cartItem.quantity;
    });

    cartSummary.textContent = `Suma: ${total.toFixed(2)} zł`;
}

function clearCart() {
    cart = [];
    updateCartUI();
}

function placeOrder() {
    alert('Twoje zamówienie zostało złożone!');
    clearCart();
}

async function loadCart() {
    const response = await fetch(origin + "/api/cart", {
        headers: {
            'Accept': 'application/json',
        },
    })
    const json = await response.json()

    if (!response.ok) {
        console.error(response, json)
    }

    cart = responseCartToCart(json);
    updateCartUI();
}

loadCart();
