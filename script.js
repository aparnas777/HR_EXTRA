document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const queryInput = document.getElementById('query-input');
    const chatHistory = document.getElementById('chat-history');
    const typingIndicator = document.getElementById('typing-indicator');
    const faqList = document.getElementById('faq-list');

    // Load FAQs immediately
    fetchFAQs();

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        // Display user message
        appendMessage('user', query);
        queryInput.value = '';

        // Show typing indicator
        typingIndicator.style.display = 'block';

        try {
            const response = await fetch('/api/user/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            // Hide typing indicator
            typingIndicator.style.display = 'none';

            // Display assistant message
            appendMessage('assistant', data.response);

        } catch (error) {
            typingIndicator.style.display = 'none';
            appendMessage('assistant', "Sorry, I'm having trouble connecting to the server right now.");
        }
    });

    function appendMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        const iconClass = role === 'user' ? 'bx-user' : 'bx-bot';

        msgDiv.innerHTML = `
            <div class="avatar"><i class='bx ${iconClass}'></i></div>
            <div class="content">${text}</div>
        `;

        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function fetchFAQs() {
        try {
            const res = await fetch('/api/user/faqs');
            if (res.ok) {
                const data = await res.json();
                renderFAQs(data.faqs);
            }
        } catch (err) {
            console.error("Could not fetch FAQs", err);
        }
    }

    function renderFAQs(faqs) {
        faqList.innerHTML = '';
        if (!faqs || faqs.length === 0) {
            faqList.innerHTML = `<p style="color: #6b7280; font-size: 0.9rem;">No FAQs available yet.</p>`;
            return;
        }

        faqs.forEach(faq => {
            const item = document.createElement('div');
            item.className = 'faq-item';
            item.innerHTML = `
                <div class="faq-question">${faq.question}</div>
                <div class="faq-answer">${faq.answer}</div>
            `;
            faqList.appendChild(item);
        });
    }
});