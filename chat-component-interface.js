// chat-component-interface.js - Enhanced ChatGPT-Style Chat Interface
// This file provides all the functionality for the chat-component-interface.htm component

(function() {
    'use strict';

    // ============================================================================
    // SESSION MANAGEMENT
    // ============================================================================

    const SESSION_STORAGE_KEYS = {
        SESSION_ID: 'its_chat_session_id',
        USER_ROLE: 'its_chat_user_role',
        LAST_ACTIVITY: 'its_chat_last_activity',
        QUERY_COUNT: 'its_chat_query_count',
        LAST_RESET_DATE: 'its_chat_last_reset_date'
    };

    const MAX_QUERIES_PER_DAY = 10;
    const MAX_QUERIES_PER_CONVERSATION = 3;

    // Railway API base URL
    // UPDATE FOR EACH PROJECT DEPLOYMENT: Change this to your deployed backend URL
    const API_BASE_URL = 'https://web-production-63bf4.up.railway.app';

    // Session state management
    let sessionState = {
        sessionId: null,
        selectedRole: null,
        conversationHistory: [],
        isActive: false,
        queryCount: 0,  // Daily query count
        remainingQueries: MAX_QUERIES_PER_DAY,
        conversationQueryCount: 0  // Queries in current conversation
    };

    // Timers used to update the loading message during slow/retry responses
    let loadingRetryTimers = [];

    // Known backend model names (mirrors GEMINI_PRO_MODEL / GEMINI_PRO_FALLBACK_MODEL in config.py)
    const LLM_PRIMARY_MODEL   = 'gemini-3.1-pro-preview';
    const LLM_FALLBACK_MODEL  = 'gemini-2.5-pro';

    // Backend retry delay schedule (mirrors _RETRY_DELAYS in main.py: [2, 5])
    // Total added latency before fallback: 0 + 2 + 5 = 7 seconds
    const LLM_RETRY_DELAYS_S = [0, 2, 5]; // seconds for each primary attempt

    /**
     * Log response timing to the console and infer what the backend likely did.
     * Thresholds are approximate: add ~2-4 s for a normal Gemini API call.
     *   < 5 s  → first attempt succeeded, no retries
     *   5-8 s  → 1-2 retries on primary model detected
     *   8-12 s → all primary retries exhausted; fallback model likely succeeded
     *   error  → all models failed (503 returned to client)
     */
    function logResponseTiming(elapsedMs, isError) {
        const secs = (elapsedMs / 1000).toFixed(2);

        if (isError) {
            console.warn(
                `[LLM] ❌ Request FAILED after ${secs}s — all retries on ` +
                `${LLM_PRIMARY_MODEL} exhausted and fallback ${LLM_FALLBACK_MODEL} also failed (503)`
            );
            return;
        }

        let modelGuess, retryNote;
        if (elapsedMs < 5000) {
            modelGuess = LLM_PRIMARY_MODEL;
            retryNote  = 'first attempt succeeded — no retries needed';
        } else if (elapsedMs < 8000) {
            modelGuess = LLM_PRIMARY_MODEL;
            retryNote  = `extended response time (~${secs}s) suggests 1-2 retries on primary model`;
        } else {
            modelGuess = `${LLM_FALLBACK_MODEL} (fallback)`;
            retryNote  = `response time (~${secs}s) exceeds primary retry budget — fallback model was likely used`;
        }

        console.log(
            `[LLM] ✅ Response received in ${secs}s\n` +
            `      Model (estimated): ${modelGuess}\n` +
            `      Note: ${retryNote}`
        );
    }

    // Generate UUID for session tracking
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Initialize or retrieve session
    function initializeSession() {
        console.log('=== Initializing Session ===');

        // Check if we need to reset (new day)
        checkAndResetIfNewDay();

        // Get or create session ID
        let sessionId = localStorage.getItem(SESSION_STORAGE_KEYS.SESSION_ID);
        if (!sessionId) {
            sessionId = generateUUID();
            localStorage.setItem(SESSION_STORAGE_KEYS.SESSION_ID, sessionId);
            console.log('Created new session ID:', sessionId);
        } else {
            console.log('Retrieved existing session ID:', sessionId);
        }
        sessionState.sessionId = sessionId;

        // Load saved role
        const savedRole = localStorage.getItem(SESSION_STORAGE_KEYS.USER_ROLE);
        if (savedRole) {
            sessionState.selectedRole = savedRole;
            console.log('Loaded saved role:', savedRole);

            // Auto-select the role chip
            const roleChip = document.querySelector(`[data-role="${savedRole}"]`);
            if (roleChip) {
                roleChip.classList.add('selected');
                updatePlaceholder(savedRole);
            }
        }

        // Load query count
        const queryCount = parseInt(localStorage.getItem(SESSION_STORAGE_KEYS.QUERY_COUNT) || '0');
        sessionState.queryCount = queryCount;
        sessionState.remainingQueries = MAX_QUERIES_PER_DAY - queryCount;
        console.log(`Query count: ${queryCount} / ${MAX_QUERIES_PER_DAY}`);

        // Update UI
        updateQueryCounter();

        // Update last activity
        updateLastActivity();
    }

    // Check if it's a new day and reset counter
    function checkAndResetIfNewDay() {
        const today = new Date().toDateString();
        const lastResetDate = localStorage.getItem(SESSION_STORAGE_KEYS.LAST_RESET_DATE);

        if (lastResetDate !== today) {
            console.log('New day detected - resetting query counter');
            localStorage.setItem(SESSION_STORAGE_KEYS.QUERY_COUNT, '0');
            localStorage.setItem(SESSION_STORAGE_KEYS.LAST_RESET_DATE, today);

            // Clear old session
            localStorage.removeItem(SESSION_STORAGE_KEYS.SESSION_ID);
            localStorage.removeItem(SESSION_STORAGE_KEYS.LAST_ACTIVITY);
        }
    }

    // Update last activity timestamp
    function updateLastActivity() {
        localStorage.setItem(SESSION_STORAGE_KEYS.LAST_ACTIVITY, new Date().toISOString());
    }

    // Save user role
    function saveUserRole(role) {
        localStorage.setItem(SESSION_STORAGE_KEYS.USER_ROLE, role);
        console.log('Saved user role:', role);
    }

    // Increment query count
    function incrementQueryCount() {
        sessionState.queryCount++;
        sessionState.remainingQueries = MAX_QUERIES_PER_DAY - sessionState.queryCount;
        localStorage.setItem(SESSION_STORAGE_KEYS.QUERY_COUNT, sessionState.queryCount.toString());
        updateQueryCounter();
        console.log(`Query count incremented: ${sessionState.queryCount} / ${MAX_QUERIES_PER_DAY}`);
    }

    // Update query counter UI (daily limit)
    function updateQueryCounter() {
        const badge = document.getElementById('query-counter-badge');
        if (!badge) return;

        const remaining = sessionState.remainingQueries;

        if (remaining === 0) {
            badge.textContent = 'Daily limit reached';
            badge.className = 'counter-badge limit-reached';
        } else if (remaining <= 3) {
            badge.textContent = `${remaining} daily ${remaining === 1 ? 'query' : 'queries'} remaining`;
            badge.className = 'counter-badge limit-warning';
        } else {
            badge.textContent = `${remaining} daily queries remaining`;
            badge.className = 'counter-badge';
        }
    }

    // Update conversation counter UI
    function updateConversationCounter() {
        const conversationBadge = document.getElementById('conversation-counter-badge');
        const followupSection = document.getElementById('followup-section');
        if (!conversationBadge) return;

        const remaining = MAX_QUERIES_PER_CONVERSATION - sessionState.conversationQueryCount;

        if (remaining === 0) {
            conversationBadge.textContent = '0 of 3 queries remaining';
            conversationBadge.className = 'counter-badge limit-reached';
            // Show limit reached state
            if (followupSection) {
                followupSection.classList.add('limit-reached');
                // Add limit message if not already there
                if (!document.getElementById('limit-message')) {
                    const limitMsg = document.createElement('div');
                    limitMsg.id = 'limit-message';
                    limitMsg.className = 'limit-message';
                    limitMsg.innerHTML = '<strong>Conversation limit reached.</strong> Click "Start New Conversation" above to continue.';
                    followupSection.insertBefore(limitMsg, followupSection.firstChild);
                }
            }
        } else if (remaining === 1) {
            conversationBadge.textContent = '1 of 3 queries remaining';
            conversationBadge.className = 'counter-badge limit-warning';
        } else {
            conversationBadge.textContent = `${remaining} of 3 queries remaining`;
            conversationBadge.className = 'counter-badge';
        }
    }

    // Reset conversation
    async function resetConversation(clearRole = false) {
        console.log('=== Resetting Conversation ===');

        const resultsContainer = document.getElementById('scoping-results');
        const resultsContent = document.getElementById('results-content');
        const initialSection = document.getElementById('initial-query-section');
        const followupSection = document.getElementById('followup-section');

        // Hide conversation, show initial query section
        resultsContainer.style.display = 'none';
        if (initialSection) initialSection.style.display = 'block';
        resultsContent.innerHTML = '';
        sessionState.conversationHistory = [];
        sessionState.isActive = false;
        sessionState.conversationQueryCount = 0;  // Reset conversation query count

        // Reset follow-up section state
        if (followupSection) {
            followupSection.classList.remove('limit-reached');
            const limitMsg = document.getElementById('limit-message');
            if (limitMsg) limitMsg.remove();
        }

        // Clear inputs
        const input = document.getElementById('scoping-input');
        const followupInput = document.getElementById('followup-input');
        if (input) input.value = '';
        if (followupInput) followupInput.value = '';

        // Always clear role on reset (user must select role for new conversation)
        sessionState.selectedRole = null;
        localStorage.removeItem(SESSION_STORAGE_KEYS.USER_ROLE);
        const roleChips = document.querySelectorAll('.role-chip');
        roleChips.forEach(chip => chip.classList.remove('selected'));
        if (input) input.placeholder = 'Select your role below, then ask a question...';
        console.log('Conversation reset (role cleared)');

        // Update UI to show conversation limit reset
        updateConversationCounter();
        updateQueryCounter();

        // Call API to reset server-side conversation state
        if (sessionState.sessionId) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/reset-conversation`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        session_id: sessionState.sessionId,
                        clear_role: true  // Always clear role
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log('Server-side conversation reset:', data);
                } else {
                    console.warn('Failed to reset server-side conversation');
                }
            } catch (error) {
                console.warn('Error resetting server-side conversation:', error);
            }
        }
    }

    // Clear all session data
    function clearAllSessionData() {
        console.log('=== Clearing All Session Data ===');

        Object.values(SESSION_STORAGE_KEYS).forEach(key => {
            localStorage.removeItem(key);
        });

        // Reset state
        sessionState = {
            sessionId: null,
            selectedRole: null,
            conversationHistory: [],
            isActive: false,
            queryCount: 0,
            remainingQueries: MAX_QUERIES_PER_DAY,
            conversationQueryCount: 0
        };

        // Clear role selection
        const roleChips = document.querySelectorAll('.role-chip');
        roleChips.forEach(chip => chip.classList.remove('selected'));

        // Reset conversation
        resetConversation();

        // Re-initialize
        initializeSession();

        console.log('All session data cleared and reset');
    }

    // ============================================================================
    // UI INTERACTION
    // ============================================================================

    // Role-specific placeholder text
    const rolePlaceholders = {
        'POLICY_MAKER': 'Ask about planning goals, service packages, strategic information...',
        'CONSULTANT': 'Ask about standards, interfaces, technical specifications...',
        'MPO_STAFF': 'Ask about planning coordination, service packages, standards...',
        'PLANNER': 'Ask about planning goals, service packages, coordination needs...',
        'ENGINEER': 'Ask about functional requirements, data flows, protocols...'
    };

    // Update placeholder text
    function updatePlaceholder(role) {
        const input = document.getElementById('scoping-input');
        if (input && rolePlaceholders[role]) {
            input.placeholder = rolePlaceholders[role];
        }
    }

    // Show error message
    function showError(message, type = 'role') {
        if (type === 'role') {
            const roleError = document.getElementById('role-error');
            const roleErrorText = document.getElementById('role-error-text');
            const roleChipsRow = document.getElementById('role-chips-row');

            if (!roleError || !roleErrorText || !roleChipsRow) return;

            roleErrorText.textContent = message;
            roleError.style.display = 'flex';
            roleChipsRow.classList.add('error');

            // Scroll to error
            roleChipsRow.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Auto-hide after 5 seconds
            setTimeout(() => {
                roleError.style.display = 'none';
                roleChipsRow.classList.remove('error');
            }, 5000);
        } else if (type === 'input') {
            const inputError = document.getElementById('input-error');
            const inputErrorText = document.getElementById('input-error-text');
            const input = document.getElementById('scoping-input');

            if (!inputError || !inputErrorText || !input) return;

            inputErrorText.textContent = message;
            inputError.style.display = 'flex';
            input.classList.add('error');
            input.focus();

            // Auto-hide after 5 seconds
            setTimeout(() => {
                inputError.style.display = 'none';
                input.classList.remove('error');
            }, 5000);
        }
    }

    // Clear error messages
    function clearErrors() {
        const roleError = document.getElementById('role-error');
        const inputError = document.getElementById('input-error');
        const roleChipsRow = document.getElementById('role-chips-row');
        const scopingInput = document.getElementById('scoping-input');

        if (roleError) roleError.style.display = 'none';
        if (inputError) inputError.style.display = 'none';
        if (roleChipsRow) roleChipsRow.classList.remove('error');
        if (scopingInput) scopingInput.classList.remove('error');
    }

    // ============================================================================
    // MESSAGE DISPLAY
    // ============================================================================

    // Add message to UI
    function addMessageToUI(content, type, role = null) {
        const resultsContent = document.getElementById('results-content');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const timestamp = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

        let headerHTML = '';
        if (type === 'user' && role) {
            const roleLabel = document.querySelector(`[data-role="${role}"] .chip-text`)?.textContent || role;
            headerHTML = `
                <div class="message-header">
                    <span class="role-badge">${roleLabel}</span>
                    <span class="timestamp">${timestamp}</span>
                </div>
            `;
        } else if (type === 'assistant') {
            headerHTML = `
                <div class="message-header">
                    <span class="role-badge">ITS Assistant</span>
                    <span class="timestamp">${timestamp}</span>
                </div>
            `;
        }

        messageDiv.innerHTML = `
            ${headerHTML}
            <div class="message-content">
                ${type === 'assistant' ? content : escapeHtml(content)}
            </div>
        `;

        resultsContent.appendChild(messageDiv);
        resultsContent.scrollTop = resultsContent.scrollHeight;
    }

    // Add loading message
    function addLoadingMessage() {
        const resultsContent = document.getElementById('results-content');
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message loading-message';
        loadingDiv.id = 'loading-message';
        loadingDiv.innerHTML = `
            <div class="progress-steps">
                <div class="progress-step active" id="loading-step-1">
                    <div class="step-dot">🔍</div>
                    <div class="step-label">Searching</div>
                </div>
                <div class="progress-connector" id="loading-connector-1"></div>
                <div class="progress-step" id="loading-step-2">
                    <div class="step-dot">📄</div>
                    <div class="step-label">Analyzing</div>
                </div>
                <div class="progress-connector" id="loading-connector-2"></div>
                <div class="progress-step" id="loading-step-3">
                    <div class="step-dot">✍️</div>
                    <div class="step-label">Generating</div>
                </div>
            </div>
            <div class="progress-bar-track">
                <div class="progress-bar-fill" id="progress-bar-fill"></div>
            </div>
            <p id="loading-status-text">Searching ITS Architecture database…</p>
            <div class="skeleton-preview">
                <div class="skeleton-line skeleton-line--long"></div>
                <div class="skeleton-line skeleton-line--medium"></div>
                <div class="skeleton-line skeleton-line--long"></div>
                <div class="skeleton-line skeleton-line--short"></div>
                <div class="skeleton-line skeleton-line--medium"></div>
            </div>
        `;
        resultsContent.appendChild(loadingDiv);
        resultsContent.scrollTop = resultsContent.scrollHeight;

        // Kick the bar to ~30% shortly after render so the transition is visible
        setTimeout(() => {
            const bar = document.getElementById('progress-bar-fill');
            if (bar) bar.style.width = '20%';
        }, 100);

        // After 12s: advance to "Analyzing" stage
        loadingRetryTimers.push(setTimeout(() => {
            const step1 = document.getElementById('loading-step-1');
            const step2 = document.getElementById('loading-step-2');
            const conn1  = document.getElementById('loading-connector-1');
            const bar    = document.getElementById('progress-bar-fill');
            const status = document.getElementById('loading-status-text');
            if (step1)  { step1.classList.remove('active'); step1.classList.add('done'); }
            if (step2)  step2.classList.add('active');
            if (conn1)  conn1.classList.add('done');
            if (bar)    bar.style.width = '62%';
            if (status) status.textContent = 'Analyzing relevant documents…';
        }, 12000));

        // After 30s: advance to "Generating" stage
        loadingRetryTimers.push(setTimeout(() => {
            const step2 = document.getElementById('loading-step-2');
            const step3 = document.getElementById('loading-step-3');
            const conn2  = document.getElementById('loading-connector-2');
            const bar    = document.getElementById('progress-bar-fill');
            const status = document.getElementById('loading-status-text');
            if (step2)  { step2.classList.remove('active'); step2.classList.add('done'); }
            if (step3)  step3.classList.add('active');
            if (conn2)  conn2.classList.add('done');
            if (bar)    bar.style.width = '88%';
            if (status) status.textContent = 'Generating response…';
        }, 30000));
    }

    // Remove loading message and cancel any pending status-update timers
    function removeLoadingMessage() {
        loadingRetryTimers.forEach(t => clearTimeout(t));
        loadingRetryTimers = [];
        const loadingMsg = document.getElementById('loading-message');
        if (loadingMsg) {
            loadingMsg.remove();
        }
    }

    // Parse and handle a non-OK fetch response; returns a structured error object
    async function parseApiError(response) {
        const status = response.status;
        let detail = null;
        try {
            const body = await response.json();
            detail = body.detail || null;
        } catch (_) { /* response body was not JSON */ }

        if (status === 503) {
            console.warn(
                `[LLM] 503 received from backend — Gemini Pro model overloaded. ` +
                `All primary retries exhausted and fallback also failed. ` +
                `Detail: ${detail || '(none)'}`
            );
        } else {
            console.error(`[LLM] API error — HTTP ${status}. Detail: ${detail || '(none)'}`);
        }

        const err = new Error(`HTTP error! status: ${status}`);
        err.status = status;
        err.detail = detail;
        return err;
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ============================================================================
    // FORM SUBMISSION
    // ============================================================================

    // Handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        console.log('=== Form Submitted ===');

        clearErrors();

        // Check daily query limit
        if (sessionState.remainingQueries === 0) {
            showError('You have reached your daily limit of 10 queries. Your limit will reset at midnight.', 'input');
            addMessageToUI('You have reached your daily limit of 10 queries. Your limit will reset at midnight.', 'error');
            return;
        }

        // Check conversation query limit
        if (sessionState.conversationQueryCount >= MAX_QUERIES_PER_CONVERSATION) {
            showError('You have reached your conversation limit. Please start a new chat to continue.', 'input');
            addMessageToUI('You have reached your conversation limit. To continue, please start a new chat by clicking the "Start New Conversation" button above.', 'error');
            return;
        }

        // Validate role selection
        if (!sessionState.selectedRole) {
            console.log('❌ No role selected');
            showError('Please select your role before submitting a question.', 'role');
            return;
        }

        const input = document.getElementById('scoping-input');
        const query = input.value.trim();

        // Validate query input
        if (!query) {
            console.log('❌ No query entered');
            showError('Please enter your question before submitting.', 'input');
            return;
        }

        console.log('✓ Role:', sessionState.selectedRole);
        console.log('✓ Query:', query);

        // Disable submit button
        const submitBtn = document.getElementById('scoping-submit-btn');
        submitBtn.disabled = true;

        // Add user message to conversation history
        sessionState.conversationHistory.push({
            role: 'user',
            content: query
        });

        // Show results container and hide initial section if first message
        const resultsContainer = document.getElementById('scoping-results');
        const initialSection = document.getElementById('initial-query-section');
        if (!sessionState.isActive) {
            resultsContainer.style.display = 'block';
            if (initialSection) initialSection.style.display = 'none';
            sessionState.isActive = true;
        }

        // Display user message
        addMessageToUI(query, 'user', sessionState.selectedRole);

        // Clear input
        input.value = '';

        // Show loading message
        addLoadingMessage();

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Call API
        try {
            const requestStartTime = performance.now();
            console.log(`[LLM] Sending request — primary model: ${LLM_PRIMARY_MODEL}`);
            console.log(`Sending API request to: ${API_BASE_URL}/api/chat`);
            console.log('Request payload:', {
                message: `Role: ${sessionState.selectedRole}\nArea of Interest: ${query}`,
                session_id: sessionState.sessionId,
                history_length: sessionState.conversationHistory.length
            });

            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: `Role: ${sessionState.selectedRole}\nArea of Interest: ${query}`,
                    current_page: window.location.pathname,
                    session_id: sessionState.sessionId,
                    conversation_history: sessionState.conversationHistory
                })
            });

            const elapsedMs = performance.now() - requestStartTime;
            console.log(`API response status: ${response.status} (${(elapsedMs / 1000).toFixed(2)}s)`);

            if (!response.ok) {
                logResponseTiming(elapsedMs, true);
                throw await parseApiError(response);
            }

            logResponseTiming(elapsedMs, false);
            const data = await response.json();
            console.log('=== API Response Received ===');
            console.log('Session ID:', data.session_id);
            console.log('Remaining queries (daily):', data.remaining_queries);
            console.log('Query count (daily):', data.query_count);
            console.log('Conversation query count:', data.conversation_query_count);
            console.log('Remaining in conversation:', data.remaining_in_conversation);

            // Remove loading message
            removeLoadingMessage();

            // Add assistant response to conversation history
            sessionState.conversationHistory.push({
                role: 'assistant',
                content: data.response
            });

            // Keep only last 8 messages (4 exchanges)
            if (sessionState.conversationHistory.length > 8) {
                sessionState.conversationHistory = sessionState.conversationHistory.slice(-8);
                console.log('Trimmed conversation history to last 8 messages');
            }

            // Display assistant response
            addMessageToUI(data.response, 'assistant');

            // Update query counts (daily and conversation)
            incrementQueryCount();
            sessionState.conversationQueryCount++;
            updateConversationCounter();
            console.log(`Conversation query count: ${sessionState.conversationQueryCount} / ${MAX_QUERIES_PER_CONVERSATION}`);

            // Update last activity
            updateLastActivity();

        } catch (error) {
            console.error('❌ Chat error:', error);
            removeLoadingMessage();

            if (error.status === 503) {
                const userMsg = error.detail ||
                    '<p><strong>The AI service is temporarily unavailable.</strong></p>' +
                    '<p>Google\'s Gemini model is experiencing high demand or a brief outage. ' +
                    'The system automatically retried before failing. Please wait a minute and try your question again.</p>';
                addMessageToUI(userMsg, 'error');
            } else {
                addMessageToUI('❌ Sorry, I encountered an error. Please try again in a moment.', 'error');
            }
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
        }
    }

    // ============================================================================
    // FOLLOW-UP FORM SUBMISSION
    // ============================================================================

    // Handle follow-up form submission
    async function handleFollowupSubmit(e) {
        e.preventDefault();
        console.log('=== Follow-up Submitted ===');

        const followupInput = document.getElementById('followup-input');
        const followupSubmitBtn = document.getElementById('followup-submit-btn');
        const query = followupInput.value.trim();

        // Validate query input
        if (!query) {
            console.log('No follow-up query entered');
            followupInput.focus();
            return;
        }

        // Check daily query limit
        if (sessionState.remainingQueries === 0) {
            addMessageToUI('You have reached your daily limit of 10 queries. Your limit will reset at midnight.', 'error');
            return;
        }

        // Check conversation query limit
        if (sessionState.conversationQueryCount >= MAX_QUERIES_PER_CONVERSATION) {
            addMessageToUI('You have reached your conversation limit. Please start a new conversation to continue.', 'error');
            return;
        }

        console.log('Follow-up query:', query);
        console.log('Using stored role:', sessionState.selectedRole);

        // Disable submit button
        followupSubmitBtn.disabled = true;
        followupInput.disabled = true;

        // Add user message to conversation history
        sessionState.conversationHistory.push({
            role: 'user',
            content: query
        });

        // Display user message (without role prefix since it's a follow-up)
        addMessageToUI(query, 'user', sessionState.selectedRole);

        // Clear input
        followupInput.value = '';

        // Show loading message
        addLoadingMessage();

        // Scroll to bottom
        const resultsContent = document.getElementById('results-content');
        resultsContent.scrollTop = resultsContent.scrollHeight;

        // Call API - send just the query (no Role: prefix), backend will use stored role
        try {
            const requestStartTime = performance.now();
            console.log(`[LLM] Sending follow-up request — primary model: ${LLM_PRIMARY_MODEL}`);

            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: query,  // Just the query, no role prefix
                    current_page: window.location.pathname,
                    session_id: sessionState.sessionId,
                    conversation_history: sessionState.conversationHistory
                })
            });

            const elapsedMs = performance.now() - requestStartTime;
            console.log(`API response status: ${response.status} (${(elapsedMs / 1000).toFixed(2)}s)`);

            if (!response.ok) {
                logResponseTiming(elapsedMs, true);
                throw await parseApiError(response);
            }

            logResponseTiming(elapsedMs, false);
            const data = await response.json();
            console.log('=== Follow-up API Response ===');
            console.log('Remaining in conversation:', data.remaining_in_conversation);

            // Remove loading message
            removeLoadingMessage();

            // Add assistant response to conversation history
            sessionState.conversationHistory.push({
                role: 'assistant',
                content: data.response
            });

            // Keep only last 8 messages (4 exchanges)
            if (sessionState.conversationHistory.length > 8) {
                sessionState.conversationHistory = sessionState.conversationHistory.slice(-8);
            }

            // Display assistant response
            addMessageToUI(data.response, 'assistant');

            // Update query counts
            incrementQueryCount();
            sessionState.conversationQueryCount++;
            updateConversationCounter();
            console.log(`Conversation query count: ${sessionState.conversationQueryCount} / ${MAX_QUERIES_PER_CONVERSATION}`);

            // Update last activity
            updateLastActivity();

            // Scroll to bottom
            resultsContent.scrollTop = resultsContent.scrollHeight;

        } catch (error) {
            console.error('❌ Follow-up error:', error);
            removeLoadingMessage();

            if (error.status === 503) {
                const userMsg = error.detail ||
                    '<p><strong>The AI service is temporarily unavailable.</strong></p>' +
                    '<p>Google\'s Gemini model is experiencing high demand or a brief outage. ' +
                    'The system automatically retried before failing. Please wait a minute and try your question again.</p>';
                addMessageToUI(userMsg, 'error');
            } else {
                addMessageToUI('❌ Sorry, I encountered an error. Please try again in a moment.', 'error');
            }
        } finally {
            // Re-enable inputs (unless limit reached)
            if (sessionState.conversationQueryCount < MAX_QUERIES_PER_CONVERSATION) {
                followupSubmitBtn.disabled = false;
                followupInput.disabled = false;
                followupInput.focus();
            }
        }
    }

    // ============================================================================
    // INITIALIZATION
    // ============================================================================

    // Initialize the interactive form
    function initializeChatInterface() {
        const form = document.getElementById('scoping-form');
        const input = document.getElementById('scoping-input');
        const roleChips = document.querySelectorAll('.role-chip');
        const resultsContainer = document.getElementById('scoping-results');
        const newConversationBtn = document.getElementById('new-conversation-btn');
        const followupForm = document.getElementById('followup-form');

        // If elements don't exist yet, wait and try again
        if (!form || !input || roleChips.length === 0) {
            console.log('Chat elements not ready yet, waiting...');
            setTimeout(initializeChatInterface, 100);
            return;
        }

        console.log('Chat interface initialized successfully!');

        // Initialize session
        initializeSession();

        // Handle role chip selection
        roleChips.forEach(chip => {
            chip.addEventListener('click', async () => {
                const role = chip.dataset.role;
                console.log('Role selected:', role);

                // Remove selected class from all chips
                roleChips.forEach(c => c.classList.remove('selected'));

                // Add selected class to clicked chip
                chip.classList.add('selected');

                // Update session state
                sessionState.selectedRole = role;

                // Save to localStorage
                saveUserRole(role);

                // Update placeholder text
                updatePlaceholder(role);

                // Clear errors
                clearErrors();

                // Focus input
                input.focus();
            });
        });

        // Handle initial form submission
        form.addEventListener('submit', handleSubmit);

        // Handle follow-up form submission
        if (followupForm) {
            followupForm.addEventListener('submit', handleFollowupSubmit);
        }

        // Handle input changes (clear error when user types)
        input.addEventListener('input', () => {
            if (input.value.trim()) {
                document.getElementById('input-error').style.display = 'none';
                input.classList.remove('error');
            }
        });

        // Handle new conversation button
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', async () => {
                if (confirm('Start a new conversation? This will clear the current chat and you will need to select your role again.')) {
                    await resetConversation();
                }
            });
        }

        // Initialize counters
        updateQueryCounter();
        updateConversationCounter();
    }

    // Start initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeChatInterface);
    } else {
        // DOM already loaded, start checking immediately
        initializeChatInterface();
    }

    // ============================================================================
    // CANVAS ANIMATION - Animated Dot Network Background
    // ============================================================================

    let canvas, ctx, dots = [];
    const dotCount = 120; // Slightly more for better thread density
    const connectionDist = 70; // Max distance for a "thread" to form

    function initCanvas() {
        canvas = document.getElementById('dotsCanvas');

        // If canvas doesn't exist yet, wait and try again
        if (!canvas) {
            console.log('Canvas not ready yet, waiting...');
            setTimeout(initCanvas, 100);
            return;
        }

        // Get context if we haven't already
        if (!ctx) {
            ctx = canvas.getContext('2d');
        }

        // Set canvas dimensions to match container
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;

        console.log('Canvas initialized:', canvas.width, 'x', canvas.height);

        // Initialize dots
        dots = [];
        for (let i = 0; i < dotCount; i++) {
            dots.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.4, // Slower, more deliberate movement
                vy: (Math.random() - 0.5) * 0.4,
                radius: 1.2
            });
        }

        // Start animation if not already running
        if (!animationRunning) {
            animationRunning = true;
            animate();
        }
    }

    let animationRunning = false;

    function animate() {
        if (!canvas || !ctx) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the threads first (so they are behind the nodes)
        for (let i = 0; i < dots.length; i++) {
            for (let j = i + 1; j < dots.length; j++) {
                const dx = dots[i].x - dots[j].x;
                const dy = dots[i].y - dots[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < connectionDist) {
                    // Calculate opacity based on distance (closer = brighter)
                    const opacity = 1 - (dist / connectionDist);
                    ctx.strokeStyle = `rgba(148, 163, 184, ${opacity * 0.4})`; // Using var(--slate-400)
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(dots[i].x, dots[i].y);
                    ctx.lineTo(dots[j].x, dots[j].y);
                    ctx.stroke();
                }
            }
        }

        // Draw and update the dots (data nodes)
        ctx.fillStyle = '#94a3b8';
        dots.forEach((dot) => {
            dot.x += dot.vx;
            dot.y += dot.vy;

            // Soft bounce off the edges
            if (dot.x < 0 || dot.x > canvas.width) dot.vx *= -1;
            if (dot.y < 0 || dot.y > canvas.height) dot.vy *= -1;

            ctx.beginPath();
            ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    // Handle window resize
    window.addEventListener('resize', () => {
        if (canvas) {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
            // Reinitialize dots with new dimensions
            dots = [];
            for (let i = 0; i < dotCount; i++) {
                dots.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    radius: 1.2
                });
            }
        }
    });

    // Start canvas initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCanvas);
    } else {
        initCanvas();
    }

})();
