// // Получение всех пользователей
// async function getUsers() {
//     // отправляет запрос и получаем ответ
//     const response = await fetch("/conversation/", {
//         method: "GET",
//         headers: {"Accept": "application/json"}
//     });
//     // если запрос прошел нормально
//     if (response.ok === true) {
//         // получаем данные
//         const conversation = await response.json();
//         const table = document.querySelector("#table");
//         users.forEach(user => table.insertAdjacentHTML("afterbegin", `<tr><th>${user["email"]}</th><th>${user["password"]}</th>${user["id"]}<th>ID</th></tr>`));
//     }
// }
//
// function back() {
//     window.location.href = '/'
// }
//
// function reg() {
//     window.location.href = '/login/'
// }
//
console.log('Кнопка была нажата!');

const startButton = document.querySelector("#start-btn");
startButton.addEventListener('click', function() {
    // Здесь добавьте код, который будет выполняться при клике на кнопку
    console.log('Кнопка была нажата!');
});