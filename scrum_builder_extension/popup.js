const grabBtn = document.getElementById("grabBtn");
grabBtn.addEventListener("click", () => {
    // Получить активную вкладку браузера
    chrome.tabs.query({active: true}, function (tabs) {
        var tab = tabs[0];
        // и если она есть, то выполнить на ней скрипт
        if (tab) {
            // Получаем элемент с id "grabBtn-h"
            getConversation()
        } else {
            alert("There are no active tabs")
        }
    })
})

// Получение всех пользователей
async function getConversation() {
    // отправляет запрос и получаем ответ
    const response = await fetch("/conversation/", {
        method: "GET",
        headers: {"Accept": "application/json"}
    });
    // если запрос прошел нормально
    if (response.ok === true) {
        // получаем данные
        const conversation = await response.json();
        let element = document.getElementById("grabBtn-h");

        // Изменяем текст элемента
        element.innerHTML = conversation;
    }
}


function back() {
    window.location.href = '/'
}

function reg() {
    window.location.href = '/login/'
}

console.log('Кнопка была нажата!');

const startButton = document.querySelector("#start-btn");
startButton.addEventListener('click', function () {
    // Здесь добавьте код, который будет выполняться при клике на кнопку
    console.log('Кнопка была нажата!');
});