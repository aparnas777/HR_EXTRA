document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation Logic ---
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = {
        'upload-section': document.getElementById('upload-section'),
        'faq-section': document.getElementById('faq-section')
    };

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const targetId = link.getAttribute('href').substring(1);
            Object.values(sections).forEach(sec => sec.style.display = 'none');
            sections[targetId].style.display = 'block';

            if (targetId === 'faq-section') {
                loadFrequentQueries();
                loadCurrentFAQs();
            }
        });
    });

    // Default view
    sections['faq-section'].style.display = 'none';

    // --- Upload Logic ---
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');
    let selectedFiles = [];

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

    function handleFiles(files) {
        selectedFiles = Array.from(files);
        fileList.innerHTML = `<p><b>Selected:</b> ${selectedFiles.map(f => f.name).join(', ')}</p>`;
    }

    uploadBtn.addEventListener('click', async () => {
        if (selectedFiles.length === 0) {
            uploadStatus.textContent = 'Please select files first.';
            uploadStatus.className = 'status-msg error';
            return;
        }

        uploadStatus.textContent = 'Uploading and indexing documents...';
        uploadStatus.className = 'status-msg';

        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files', file));

        try {
            const response = await fetch('/api/admin/upload-doc', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                uploadStatus.textContent = data.message;
                uploadStatus.className = 'status-msg success';
                selectedFiles = [];
                fileList.innerHTML = '';
            } else {
                throw new Error(data.detail);
            }
        } catch (error) {
            uploadStatus.textContent = 'Upload failed: ' + error.message;
            uploadStatus.className = 'status-msg error';
        }
    });

    // --- FAQ Logic ---
    const faqForm = document.getElementById('add-faq-form');
    const faqStatus = document.getElementById('faq-status');
    const queriesList = document.getElementById('frequent-queries');
    const currentFaqsList = document.getElementById('current-faqs');

    faqForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = document.getElementById('faq-question').value;
        const answer = document.getElementById('faq-answer').value;

        addFAQ(question, answer, 'admin');
    });

    async function addFAQ(question, answer, source = 'admin') {
        try {
            const res = await fetch('/api/admin/faq', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, answer, source })
            });
            const data = await res.json();

            if (res.ok) {
                faqStatus.textContent = 'FAQ added successfully!';
                faqStatus.className = 'status-msg success';
                faqForm.reset();
                loadCurrentFAQs();
            } else {
                throw new Error(data.detail);
            }
        } catch (err) {
            faqStatus.textContent = 'Error: ' + err.message;
            faqStatus.className = 'status-msg error';
        }
    }

    async function loadFrequentQueries() {
        try {
            const res = await fetch('/api/admin/frequent-queries');
            const data = await res.json();

            if (data.queries && data.queries.length > 0) {
                queriesList.innerHTML = data.queries.map(q => `
                    <div class="query-item">
                        <div>
                            <strong>${q.query}</strong>
                            <span class="badge">Asked ${q.frequency} times</span>
                        </div>
                        <button class="promote-btn" onclick="promoteQuery('${q.query.replace(/'/g, "\\'")}')">
                            <i class='bx bx-plus'></i> Add Answer
                        </button>
                    </div>
                `).join('');
            } else {
                queriesList.innerHTML = '<p class="text-muted">No frequent queries found yet.</p>';
            }
        } catch (e) {
            console.error('Error fetching frequent queries');
        }
    }

    async function loadCurrentFAQs() {
        try {
            const res = await fetch('/api/user/faqs'); // Reusing user endpoint for simplicity
            if (res.ok) {
                const data = await res.json();
                renderCurFAQs(data.faqs);
            }
        } catch (err) {
            console.error(err);
        }
    }

    function renderCurFAQs(faqs) {
        if (!faqs || faqs.length === 0) {
            currentFaqsList.innerHTML = `<p class="text-muted">No FAQs present.</p>`;
            return;
        }
        currentFaqsList.innerHTML = faqs.map(faq => `
            <div class="faq-item">
                <div style="font-weight: 600; font-size: 14px;">${faq.question}</div>
                <div style="font-size: 13px; color: #666; margin-top: 4px;">${faq.answer}</div>
                <div style="font-size: 11px; color: #999; margin-top: 6px;">Source: ${faq.source}</div>
            </div>
        `).join('');
    }

    // Global function for the inline onclick handler
    window.promoteQuery = function (queryText) {
        document.getElementById('faq-question').value = queryText;
        document.getElementById('faq-answer').focus();
    };
});