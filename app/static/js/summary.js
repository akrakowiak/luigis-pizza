const pizzaTemplate = document.getElementById("pizza-template");
const pizzasContainer = document.getElementById("pizzas-container");

const pizzaToElement = (pizzaData) => {
  const { name } = pizzaData;
  const pizza = pizzaTemplate.content.cloneNode(true);
  pizza.querySelector(".pizza-test").innerHTML = name;
  return pizza;
}

pizzasContainer.appendChild(pizzaToElement({name: "Example of using templates"}));
