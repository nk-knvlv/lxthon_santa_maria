class ScrumBuilder {
    constructor() {
        this.addListeners()
    }

    addListeners() {
        const masterInviteBtn = document.getElementById("start");
        masterInviteBtn.addEventListener("click", async () => {
            console.log('test1')
            const meetLinkInput = document.getElementById("meet-link");
            const meetId = meetLinkInput.value.split('/')[3]
            await this.inviteMaster(meetId)

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

