const currentDate = new Date()
const currentDateStr = currentDate.toISOString().slice(0, 16);

const bookDatetime = document.querySelector("#book-datetime");

const onTableClick = (event) => {
  const tableName = event.target.dataset.tableName;
  console.log(`Table ${tableName} clicked`);
}

const onDateInput = (event) => {
  console.log("Date changed");
}

const onSubmit = (event) => {
  event.preventDefault();

  const bookDate = new Date(bookDatetime.value);
  const dateInvalid = !bookDate.valueOf();

  if (dateInvalid || bookDate < currentDate) {
    console.log("Invalid date:", bookDate);
    return;
  }

  console.log("Submit clicked");
}

bookDatetime.min = currentDateStr;
