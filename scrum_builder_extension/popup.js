class ScrumBuilder {
    constructor() {
        this.meetIdInput = document.getElementById("meet-link");
        this.statusElement = document.getElementById("status");
        this.conversationLog = document.getElementById("conversationLog");
        this.aiResponseContent = document.getElementById("aiResponseContent");
        this.helpMenu = document.getElementById("helpMenu");
        this.startBtn = document.getElementById("start");
        this.breakBtn = document.getElementById("break_call");
        this.autoRefreshToggle = document.getElementById("autoRefresh");
        this.pasteBtn = document.getElementById("pasteBtn");
        this.conversationTab = document.getElementById("conversationTab");
        this.analysisTab = document.getElementById("analysisTab");
        this.conversationPanel = document.getElementById("conversationPanel");
        this.analysisPanel = document.getElementById("analysisPanel");
        this.updateInterval = null;
        this.isActive = false;
        this.lastUpdateTime = null;
        this.updateFrequency = 60; // 60 секунд (1 минута)

        this.aiStatusInterval = null;
        this.aiStatusElement = document.createElement('div');
        this.aiStatusElement.className = 'ai-status';
        document.querySelector('.panel-header').appendChild(this.aiStatusElement);

        this.init();
    }

    async init() {
        this.addListeners();
        await this.checkActiveSession();
        this.setupAutoRefresh();
        this.startAIStatusUpdates();
    }

    async checkActiveSession() {
        try {
            const response = await this.apiRequest('GET', '/status');
            if (response.active) {
                this.setActiveState(true);
                this.startUpdates();
            }
        } catch (error) {
            console.log("No active session:", error);
        }
    }

    setupAutoRefresh() {
        chrome.storage.sync.get(['refreshInterval'], (result) => {
            if (result.refreshInterval) {
                this.updateFrequency = result.refreshInterval;
            }
            if (this.autoRefreshToggle) {
                this.autoRefreshToggle.checked = true;
            }
        });
    }

    async checkAIStatus() {
        try {
            const response = await this.apiRequest('GET', '/ai-response/status');
            this.updateAIStatusUI(response);
        } catch (error) {
            console.error('AI status check failed:', error);
            this.aiStatusElement.textContent = 'AI Status: Offline';
            this.aiStatusElement.style.color = '#e74c3c';
        }
    }

    updateAIStatusUI(status) {
        this.aiStatusElement.textContent = `AI Status: ${status.state || 'Unknown'}`;
        this.aiStatusElement.style.color =
            status.state === 'Ready' ? '#2ecc71' :
            status.state === 'Processing' ? '#f39c12' : '#e74c3c';

        if (status.details) {
            this.aiStatusElement.title = status.details;
        }
    }

    async apiRequest(method, endpoint, data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(`http://localhost:8000${endpoint}`, options);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request error (${endpoint}):`, error);
            throw error;
        }
    }

    addListeners() {
        this.startBtn.addEventListener("click", () => this.handleStart());
        this.breakBtn.addEventListener("click", () => this.handleBreak());

        this.pasteBtn.addEventListener("click", async () => {
            try {
                const text = await navigator.clipboard.readText();
                if (text.includes("meet.google.com")) {
                    this.meetIdInput.value = text;
                }
            } catch (error) {
                this.setStatus("Failed to paste from clipboard", "error");
            }
        });

        this.autoRefreshToggle.addEventListener("change", () => {
            if (this.autoRefreshToggle.checked && this.isActive) {
                this.startUpdates();
            } else {
                this.stopUpdates();
            }
        });

        document.getElementById("menuBtn").addEventListener("click", () => {
            this.helpMenu.classList.toggle("hidden");
            this.helpMenu.setAttribute("aria-hidden",
                this.helpMenu.classList.contains("hidden"));
        });

        document.getElementById("closeHelp").addEventListener("click", () => {
            this.helpMenu.classList.add("hidden");
            this.helpMenu.setAttribute("aria-hidden", "true");
        });

        this.conversationTab.addEventListener("click", () => this.switchTab('conversation'));
        this.analysisTab.addEventListener("click", () => this.switchTab('analysis'));
    }

    switchTab(tabName) {
        if (tabName === 'conversation') {
            this.conversationTab.classList.add('active');
            this.analysisTab.classList.remove('active');
            this.conversationPanel.classList.add('active');
            this.analysisPanel.classList.remove('active');
        } else {
            this.conversationTab.classList.remove('active');
            this.analysisTab.classList.add('active');
            this.conversationPanel.classList.remove('active');
            this.analysisPanel.classList.add('active');
        }
    }

    async handleStart() {
        this.setStatus("Processing...");
        let meetId = this.meetIdInput.value.trim();
        meetId = this.normalizeMeetId(meetId);

        if (!this.validateMeetId(meetId)) {
            this.setStatus("Please enter a valid Google Meet link", "error");
            return;
        }

        try {
            const result = await this.inviteMaster(meetId);
            if (result.success) {
                this.setStatus("Scrum Master invited successfully!", "success");
                this.setActiveState(true);
                if (this.autoRefreshToggle.checked) {
                    this.startUpdates();
                }
            } else {
                this.setStatus(result.error || "Failed to invite", "error");
            }
        } catch (error) {
            this.setStatus(error.message || "Failed to invite", "error");
            console.error("Invite error:", error);
        }
    }

    async handleBreak() {
        this.setStatus("Ending meeting...");
        try {
            const result = await this.breakMaster();
            if (result.success) {
                this.setStatus("Meeting ended successfully!", "success");
                this.setActiveState(false);
                this.stopUpdates();
                this.clearConversationLog();
            } else {
                this.setStatus(result.error || "Failed to end meeting", "error");
            }
        } catch (error) {
            this.setStatus(error.message || "Failed to end meeting", "error");
            console.error("Break meeting error:", error);
        }
    }

    setActiveState(isActive) {
        this.isActive = isActive;
        this.startBtn.disabled = isActive;
        this.breakBtn.disabled = !isActive;
        this.meetIdInput.disabled = isActive;

        const emptyState = document.querySelector(".empty-state");
        if (emptyState) {
            emptyState.style.display = isActive ? "none" : "flex";
        }
    }

    startUpdates() {
        this.stopUpdates();
        this.fetchMeetingData();

        this.updateInterval = setInterval(
            () => this.fetchMeetingData(),
            this.updateFrequency * 1000
        );

        console.log(`Started updates every ${this.updateFrequency} seconds`);
    }

    stopUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        if (this.aiStatusInterval) {
            clearInterval(this.aiStatusInterval);
            this.aiStatusInterval = null;
        }
    }

    async fetchMeetingData() {
        if (!this.isActive) return;

        try {
            const [conversation, aiResponse] = await Promise.all([
                this.apiRequest('GET', '/dialog'),
                this.apiRequest('POST', '/ai-response', { conversation: [] })
            ]);

            this.updateUI(conversation, aiResponse);
            this.lastUpdateTime = new Date();
            this.setStatus(`Last updated: ${this.lastUpdateTime.toLocaleTimeString()}`, "info");
        } catch (error) {
            console.error("Failed to update meeting data:", error);
            this.setStatus("Update failed - retrying...", "error");
        }
    }

    updateUI(conversation, aiResponse) {
        // Очищаем предыдущие сообщения
        this.conversationLog.innerHTML = '';

        // Добавляем новые сообщения
        conversation.forEach(msg => {
            const msgElement = document.createElement("div");
            msgElement.className = "message user-message";
            msgElement.innerHTML = `
                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                ${msg}
            `;
            this.conversationLog.appendChild(msgElement);
        });

        // Обновляем ответ ИИ
        if (aiResponse && aiResponse.success) {
            this.aiResponseContent.innerHTML = `
                <div class="message ai-message">
                    <span class="timestamp">${new Date().toLocaleTimeString()}</span>
                    ${aiResponse.text}
                </div>
            `;
        } else {
            this.aiResponseContent.innerHTML = `
                <div class="empty-state">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.516 6.516 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5z"/>
                    </svg>
                    <p>No AI analysis available</p>
                </div>
            `;
        }
    }

    clearConversationLog() {
        this.conversationLog.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                <p>No active meeting analysis</p>
            </div>
        `;
        this.aiResponseContent.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.516 6.516 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5z"/>
                </svg>
                <p>No AI analysis available</p>
            </div>
        `;
    }

    normalizeMeetId(meetId) {
        if (!meetId) return meetId;
        if (meetId.includes("meet.google.com/")) {
            const parts = meetId.split("/");
            meetId = parts[parts.length - 1].split("?")[0];
        }
        return meetId.trim();
    }

    validateMeetId(meetId) {
        return meetId && meetId.length >= 3 && /^[a-z0-9-]+$/i.test(meetId);
    }

    setStatus(message, type = "info") {
        this.statusElement.textContent = message;
        this.statusElement.style.color =
            type === "error" ? "#e74c3c" :
            type === "success" ? "#2ecc71" : "#7f8c8d";
    }

    async inviteMaster(meet_id) {
        return this.apiRequest('POST', '/start', { meet_id });
    }

    async breakMaster() {
        return this.apiRequest('POST', '/leave');
    }

    startAIStatusUpdates() {
        this.checkAIStatus();
        this.aiStatusInterval = setInterval(
            () => this.checkAIStatus(),
            30000
        );
    }
}

new ScrumBuilder();