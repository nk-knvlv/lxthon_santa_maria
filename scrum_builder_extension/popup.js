const grabBtn = document.getElementById("grabBtn");

grabBtn.addEventListener("click", () => {
    chrome.tabs.query({active: true}, async function (tabs) {
        let tab = tabs[0];
        if (tab) {
            let conn = document.getElementById("conn");
            conn.innerHTML = 'false';

            try {
                const response = await fetch("http://localhost:8000/test", {
                    method: "GET",
                    headers: {"Accept": "text/plain"}
                });

                if (response.ok) {
                    const text = await response.text(); // получаем текст ответа
                    console.log(text); // выводим в консоль
                    conn.innerHTML = 'success';

                    let result = document.getElementById("result");
                    result.innerHTML = text;
                } else {
                    console.error("HTTP error", response.status);
                    conn.innerHTML = 'error';
                }
            } catch (error) {
                console.error("Fetch error:", error);
                conn.innerHTML = 'fetch error';
            }
        } else {
            alert("There are no active tabs");
        }
    });
});
