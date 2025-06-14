class ScrumBuilder {
    constructor() {
        this.addListeners()
    }

    addListeners() {
        const masterInviteBtn = document.getElementById("start");
        masterInviteBtn.addEventListener("click", async () => {
            console.log('test1')
            const meetIdInput = document.getElementById("meet-id");
            const meetId = meetIdInput.value
            await this.inviteMaster(meetId)

        });
    }

    static test() {
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
    }

    async inviteMaster(meet_id) {
        const response = await fetch("http://localhost:8000/start", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "text/plain"
            },
            body: JSON.stringify({meet_id: meet_id}) // добавляем тело запроса с параметром meet_id
        })
    }
}


const scrumMaster = new ScrumBuilder();
// scrumMaster.test()

