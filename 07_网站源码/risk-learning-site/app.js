/**
 * 商业风险处置学习站 - 主应用逻辑 v3
 * 多文件数据架构：data.js 索引 + data-*.js 分栏目数据
 */

(function() {
    'use strict';

    // ========== DOM ==========
    const $ = id => document.getElementById(id);
    const navTree = $('nav-tree');
    const searchInput = $('search-input');
    const searchResults = $('search-results');
    const articleTitle = $('article-title');
    const articleMeta = $('article-meta');
    const articleBody = $('article-body');
    const breadcrumb = $('breadcrumb');
    const articleNav = $('article-nav');
    const menuToggle = $('menu-toggle');
    const sidebar = $('sidebar');
    const overlay = $('overlay');
    const lastUpdated = $('last-updated');

    // ========== State ==========
    let currentArticleId = null;
    let flatArticles = [];  // all articles flattened for search/nav
    let allArticleMap = {}; // id -> article object
    
    // Check-in state (localStorage)
    const CHECKIN_KEY = 'risk-learning-checkin';
    let checkinState = loadCheckinState();

    // ========== Init ==========
    function init() {
        if (typeof SITE_DATA === 'undefined') {
            showError('Data load failed: SITE_DATA not found');
            return;
        }

        buildArticleIndex();
        renderNav();
        setupSearch();
        setupMobileMenu();
        setupHashRouter();
        updateSidebarProgress();

        if (lastUpdated && SITE_DATA.site.lastUpdated) {
            lastUpdated.textContent = 'Updated: ' + SITE_DATA.site.lastUpdated;
        }

        // Initial load from hash
        const hash = location.hash.slice(1);
        if (hash && allArticleMap[hash]) {
            loadArticle(hash);
        } else {
            showWelcome();
        }
    }

    // ========== Build flat article list from all data modules ==========
    function buildArticleIndex() {
        flatArticles = [];
        allArticleMap = {};

        SITE_DATA.sections.forEach(section => {
            const dataModule = SITE_DATA[section.dataRef];
            if (!dataModule || !dataModule.articles) return;

            Object.values(dataModule.articles).forEach(article => {
                const flat = {
                    ...article,
                    sectionId: section.id,
                    sectionTitle: section.title,
                    sectionIcon: section.icon
                };
                flatArticles.push(flat);
                allArticleMap[article.id] = flat;
            });
        });
    }

    // ========== Render sidebar navigation ==========
    function renderNav() {
        navTree.innerHTML = '';

        SITE_DATA.sections.forEach(section => {
            const dataModule = SITE_DATA[section.dataRef];
            if (!dataModule) return;

            const articles = dataModule.articles ? Object.values(dataModule.articles) : [];
            const subsections = dataModule.subsections || [];

            const sectionEl = document.createElement('div');
            sectionEl.className = 'nav-section';
            sectionEl.dataset.section = section.id;

            // Section title
            const titleEl = document.createElement('div');
            titleEl.className = 'nav-section-title';
            const articleCount = articles.length;
            titleEl.innerHTML = `<span>${section.icon} ${escapeHtml(section.title)}${articleCount > 0 ? ' <em>(' + articleCount + ')</em>' : ''}</span><span class="nav-toggle-icon">\u25BC</span>`;
            titleEl.addEventListener('click', () => {
                sectionEl.classList.toggle('collapsed');
            });

            const articlesEl = document.createElement('div');
            articlesEl.className = 'nav-articles';

            if (articles.length === 0) {
                // Show placeholder for empty sections
                const placeholder = document.createElement('div');
                placeholder.className = 'nav-item nav-placeholder';
                placeholder.textContent = 'Coming soon...';
                placeholder.style.cursor = 'default';
                placeholder.style.opacity = '0.4';
                articlesEl.appendChild(placeholder);
            } else {
                // Group by subsection if available
                const grouped = {};
                articles.forEach(a => {
                    const sub = a.subsection || 'other';
                    if (!grouped[sub]) grouped[sub] = [];
                    grouped[sub].push(a);
                });

                // If only one subsection or no subsections, flat list
                const subKeys = Object.keys(grouped);
                if (subKeys.length <= 1) {
                    articles.forEach(article => {
                        articlesEl.appendChild(createNavItem(article));
                    });
                } else {
                    // Show subsection headers
                    subsections.forEach(sub => {
                        if (grouped[sub.id] && grouped[sub.id].length > 0) {
                            const subHeader = document.createElement('div');
                            subHeader.className = 'nav-subsection-title';
                            subHeader.textContent = sub.title;
                            articlesEl.appendChild(subHeader);
                            grouped[sub.id].forEach(article => {
                                articlesEl.appendChild(createNavItem(article));
                            });
                        }
                    });
                }
            }

            sectionEl.appendChild(titleEl);
            sectionEl.appendChild(articlesEl);
            navTree.appendChild(sectionEl);
        });
    }

    function createNavItem(article) {
        const item = document.createElement('div');
        item.className = 'nav-item';
        item.dataset.id = article.id;
        item.textContent = article.title;
        item.addEventListener('click', () => {
            loadArticle(article.id);
            closeMobileMenu();
        });
        return item;
    }

    // ========== Search ==========
    function setupSearch() {
        searchInput.addEventListener('input', debounce(e => {
            const query = e.target.value.trim().toLowerCase();
            if (!query) {
                searchResults.classList.remove('active');
                return;
            }

            const results = flatArticles.filter(a => {
                const text = [
                    a.title,
                    (a.tags || []).join(' '),
                    a.summary || '',
                    a.difficulty || '',
                    a.week || ''
                ].join(' ').toLowerCase();
                return text.includes(query);
            }).slice(0, 12);

            renderSearchResults(results, query);
        }, 250));

        document.addEventListener('click', e => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove('active');
            }
        });
    }

    function renderSearchResults(results, query) {
        searchResults.innerHTML = '';
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item"><span class="search-result-title">No matches</span></div>';
        } else {
            results.forEach(r => {
                const div = document.createElement('div');
                div.className = 'search-result-item';
                const tags = (r.tags || []).map(t => `<span class="search-tag">${escapeHtml(t)}</span>`).join(' ');
                div.innerHTML = `
                    <div class="search-result-title">${highlightText(r.title, query)}</div>
                    <div class="search-result-section">${escapeHtml(r.sectionTitle)} ${tags}</div>
                    ${r.summary ? '<div class="search-result-summary">' + highlightText(escapeHtml(r.summary.substring(0, 80)) + '...', query) + '</div>' : ''}
                `;
                div.addEventListener('click', () => {
                    loadArticle(r.id);
                    searchResults.classList.remove('active');
                    searchInput.value = '';
                    closeMobileMenu();
                });
                searchResults.appendChild(div);
            });
        }
        searchResults.classList.add('active');
    }

    function highlightText(text, query) {
        if (!query) return text;
        const regex = new RegExp('(' + escapeRegex(query) + ')', 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    // ========== Load Article ==========
    function loadArticle(id) {
        const article = allArticleMap[id];
        if (!article) return;

        currentArticleId = id;
        location.hash = id;

        // Title
        articleTitle.textContent = article.title;

        // Meta: tags + difficulty + week + source
        articleMeta.innerHTML = '';
        if (article.tags && article.tags.length) {
            article.tags.forEach(tag => {
                const span = document.createElement('span');
                span.className = 'article-tag';
                if (tag === 'entry') span.classList.add('tag-entry');
                else if (tag === 'advanced') span.classList.add('tag-advanced');
                else if (tag === 'expert') span.classList.add('tag-expert');
                span.textContent = tag;
                articleMeta.appendChild(span);
            });
        }
        if (article.week) {
            const weekSpan = document.createElement('span');
            weekSpan.className = 'article-week';
            weekSpan.textContent = article.week;
            articleMeta.appendChild(weekSpan);
        }
        if (article.source) {
            const srcSpan = document.createElement('span');
            srcSpan.className = 'article-source';
            srcSpan.textContent = article.source;
            articleMeta.appendChild(srcSpan);
        }
        if (article.updated) {
            const dateSpan = document.createElement('span');
            dateSpan.className = 'article-date';
            dateSpan.textContent = article.updated;
            articleMeta.appendChild(dateSpan);
        }

        // Breadcrumb
        const section = SITE_DATA.sections.find(s => s.dataRef && SITE_DATA[s.dataRef] && SITE_DATA[s.dataRef].articles && SITE_DATA[s.dataRef].articles[id]);
        let subsecTitle = '';
        if (section && article.subsection) {
            const dm = SITE_DATA[section.dataRef];
            if (dm && dm.subsections) {
                const sub = dm.subsections.find(s => s.id === article.subsection);
                if (sub) subsecTitle = sub.title;
            }
        }
        let crumbHtml = `<a onclick="loadArticle('')">Home</a><span class="breadcrumb-separator">/</span>`;
        if (section) {
            crumbHtml += `<span>${escapeHtml(section.title)}</span>`;
            if (subsecTitle) {
                crumbHtml += `<span class="breadcrumb-separator">/</span><span>${escapeHtml(subsecTitle)}</span>`;
            }
        }
        crumbHtml += `<span class="breadcrumb-separator">/</span><span>${escapeHtml(article.title)}</span>`;
        breadcrumb.innerHTML = crumbHtml;

        // Content
        if (article.contentHtml) {
            articleBody.innerHTML = article.contentHtml.replace(/\\n/g, '\n');
        } else if (article.content) {
            articleBody.innerHTML = simpleMarkdownToHtml(article.content);
        } else {
            articleBody.innerHTML = '<p class="empty-content">Content pending</p>';
        }
        
        // Add check-in button at the end of article
        const completed = isCompleted(id);
        const checkinBtn = document.createElement('div');
        checkinBtn.className = 'article-checkin-section';
        checkinBtn.innerHTML = `
            <button class="checkin-btn ${completed ? 'completed' : ''}" 
                    data-article="${id}" 
                    onclick="toggleCheckin('${id}')">
                ${completed ? '✓ Completed' : 'Mark as Complete'}
            </button>
        `;
        articleBody.appendChild(checkinBtn);

        // Nav highlight
        document.querySelectorAll('.nav-item').forEach(el => {
            el.classList.toggle('active', el.dataset.id === id);
        });

        // Expand parent section
        const activeSection = document.querySelector('.nav-section:has(.nav-item[data-id="' + id + '"])');
        if (activeSection) {
            activeSection.classList.remove('collapsed');
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Prev/Next nav
        renderArticleNav(id);
    }

    // ========== Welcome Page ==========
    function showWelcome() {
        currentArticleId = null;
        location.hash = '';
        articleTitle.textContent = 'Welcome';
        articleMeta.innerHTML = '';
        breadcrumb.innerHTML = '<span>Home</span>';

        let cardsHtml = '';
        SITE_DATA.sections.forEach(section => {
            const dm = SITE_DATA[section.dataRef];
            const count = (dm && dm.articles) ? Object.keys(dm.articles).length : 0;
            const statusLabel = count > 0 ? count + ' articles' : 'Pending';
            cardsHtml += `
                <div class="welcome-card ${count === 0 ? 'welcome-card-pending' : ''}">
                    <div class="welcome-card-icon">${section.icon}</div>
                    <h3>${escapeHtml(section.title)}</h3>
                    <p>${statusLabel}</p>
                </div>
            `;
        });

        // Calculate overall progress
        const totalArticles = flatArticles.length;
        const completedArticles = checkinState.completed.length;
        const progressPercent = totalArticles > 0 ? Math.round((completedArticles / totalArticles) * 100) : 0;

        articleBody.innerHTML = `
            <div class="welcome-content">
                <h2>Commercial Risk Management</h2>
                <p>Knowledge Deposit / Knowledge Base / Knowledge Learning - Three in One<br>
                Based on 19 content assets, covering 6 sections, 13-week growth path.</p>
                
                <!-- Progress Overview -->
                <div class="progress-overview">
                    <div class="progress-stats">
                        <div class="stat-item">
                            <strong>${completedArticles}/${totalArticles}</strong>
                            <span>Articles Completed</span>
                        </div>
                        <div class="stat-item">
                            <strong>${progressPercent}%</strong>
                            <span>Overall Progress</span>
                        </div>
                        <div class="stat-item">
                            <strong>${SITE_DATA.sections.length}</strong>
                            <span>Sections</span>
                        </div>
                        <div class="stat-item">
                            <strong>13</strong>
                            <span>Weeks Path</span>
                        </div>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${progressPercent}%"></div>
                    </div>
                </div>
                
                <div class="welcome-cards">
                    ${cardsHtml}
                </div>
                
                <!-- Learning Path Timeline -->
                <div class="timeline-section">
                    <h3>13-Week Learning Path</h3>
                    ${renderTimeline()}
                </div>
            </div>
        `;

        articleNav.innerHTML = '';
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    }

    // ========== Prev/Next Navigation ==========
    function renderArticleNav(currentId) {
        const idx = flatArticles.findIndex(a => a.id === currentId);
        if (idx === -1) return;

        let html = '';
        if (idx > 0) {
            const prev = flatArticles[idx - 1];
            html += `<a class="nav-prev" onclick="loadArticle('${prev.id}')"><div class="nav-label">\u2190 Prev</div><div class="nav-title">${escapeHtml(prev.title)}</div></a>`;
        } else {
            html += '<div></div>';
        }

        if (idx < flatArticles.length - 1) {
            const next = flatArticles[idx + 1];
            html += `<a class="nav-next" onclick="loadArticle('${next.id}')"><div class="nav-label">Next \u2192</div><div class="nav-title">${escapeHtml(next.title)}</div></a>`;
        } else {
            html += '<div></div>';
        }

        articleNav.innerHTML = html;
    }

    // ========== Mobile Menu ==========
    function setupMobileMenu() {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
        });
        overlay.addEventListener('click', closeMobileMenu);
    }

    function closeMobileMenu() {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
    }

    // ========== Hash Router ==========
    function setupHashRouter() {
        window.addEventListener('hashchange', () => {
            const hash = location.hash.slice(1);
            if (hash && allArticleMap[hash]) {
                loadArticle(hash);
            } else if (!hash) {
                showWelcome();
            }
        });
    }

    // ========== Check-in State Management ==========
    function loadCheckinState() {
        try {
            const data = localStorage.getItem(CHECKIN_KEY);
            return data ? JSON.parse(data) : { completed: [], lastCheckin: null };
        } catch (e) {
            return { completed: [], lastCheckin: null };
        }
    }

    function saveCheckinState() {
        try {
            localStorage.setItem(CHECKIN_KEY, JSON.stringify(checkinState));
        } catch (e) {
            console.warn('Failed to save checkin state:', e);
        }
    }

    function toggleCheckin(articleId) {
        const idx = checkinState.completed.indexOf(articleId);
        if (idx === -1) {
            checkinState.completed.push(articleId);
            checkinState.lastCheckin = new Date().toISOString();
        } else {
            checkinState.completed.splice(idx, 1);
        }
        saveCheckinState();
        updateCheckinUI(articleId);
        updateSidebarProgress();
    }

    function isCompleted(articleId) {
        return checkinState.completed.includes(articleId);
    }

    function getWeekProgress(weekId) {
        if (!SITE_DATA.path || !SITE_DATA.path.weeks) return { total: 0, completed: 0 };
        const weekData = SITE_DATA.path.weeks[weekId];
        if (!weekData || !weekData.articles) return { total: 0, completed: 0 };
        const total = weekData.articles.length;
        const completed = weekData.articles.filter(id => isCompleted(id)).length;
        return { total, completed };
    }

    // ========== Utilities ==========
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function debounce(fn, ms) {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), ms);
        };
    }

    function simpleMarkdownToHtml(md) {
        if (!md) return '';
        let html = escapeHtml(md);
        html = html.replace(/^#{6}\s+(.+)$/gm, '<h6>$1</h6>');
        html = html.replace(/^#{5}\s+(.+)$/gm, '<h5>$1</h5>');
        html = html.replace(/^#{4}\s+(.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^#{3}\s+(.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^#{2}\s+(.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^#{1}\s+(.+)$/gm, '<h1>$1</h1>');
        html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/^&gt;\s?(.+)$/gm, '<blockquote>$1</blockquote>');
        html = html.replace(/^[-*+]\s+(.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
        html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
        html = html.replace(/^---$/gm, '<hr>');
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
        const lines = html.split('\n');
        let result = '';
        for (let line of lines) {
            line = line.trim();
            if (!line) continue;
            if (line.startsWith('<h') || line.startsWith('<blockquote') ||
                line.startsWith('<ul') || line.startsWith('<li') ||
                line.startsWith('<hr') || line.startsWith('<pre')) {
                result += line + '\n';
            } else {
                result += '<p>' + line + '</p>\n';
            }
        }
        return result;
    }

    function showError(msg) {
        articleBody.innerHTML = '<div style="color:#e53e3e;padding:40px;text-align:center;"><h2>Error</h2><p>' + escapeHtml(msg) + '</p></div>';
    }

    // ========== Timeline Rendering ==========
    function renderTimeline() {
        if (!SITE_DATA.path || !SITE_DATA.path.weeks) return '<p class="empty-content">Timeline data pending</p>';
        
        const phases = SITE_DATA.path.phases || [];
        const weeks = SITE_DATA.path.weeks;
        
        let html = '<div class="timeline">';
        
        phases.forEach(phase => {
            const phaseWeeks = phase.weeks.split('-');
            const startWeek = parseInt(phaseWeeks[0].substring(1));
            const endWeek = parseInt(phaseWeeks[1].substring(1));
            
            html += `
                <div class="timeline-phase" style="--phase-color: ${phase.color}">
                    <div class="phase-header">
                        <h4>${escapeHtml(phase.title)}</h4>
                        <span class="phase-weeks">${phase.weeks}</span>
                    </div>
                    <div class="phase-weeks-grid">
            `;
            
            for (let w = startWeek; w <= endWeek; w++) {
                const weekId = 'W' + w;
                const weekData = weeks[weekId];
                if (!weekData) continue;
                
                const progress = getWeekProgress(weekId);
                const progressPercent = progress.total > 0 ? Math.round((progress.completed / progress.total) * 100) : 0;
                const isComplete = progress.completed === progress.total && progress.total > 0;
                
                html += `
                    <div class="timeline-week ${isComplete ? 'week-complete' : ''}">
                        <div class="week-header">
                            <span class="week-number">${weekId}</span>
                            <span class="week-title">${escapeHtml(weekData.title)}</span>
                        </div>
                        <div class="week-progress">
                            <div class="week-progress-bar" style="width: ${progressPercent}%"></div>
                        </div>
                        <div class="week-articles">
                            ${weekData.articles.map(articleId => {
                                const article = allArticleMap[articleId];
                                const completed = isCompleted(articleId);
                                if (!article) return '';
                                return `
                                    <div class="timeline-article ${completed ? 'article-complete' : ''}" 
                                         onclick="loadArticle('${articleId}')" 
                                         title="${escapeHtml(article.title)}">
                                        <span class="article-check">${completed ? '✓' : '○'}</span>
                                        <span class="article-name">${escapeHtml(article.title.substring(0, 30))}${article.title.length > 30 ? '...' : ''}</span>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }
            
            html += '</div></div>';
        });
        
        html += '</div>';
        return html;
    }

    // ========== Check-in UI Updates ==========
    function updateCheckinUI(articleId) {
        const btn = document.querySelector(`.checkin-btn[data-article="${articleId}"]`);
        if (btn) {
            const completed = isCompleted(articleId);
            btn.classList.toggle('completed', completed);
            btn.textContent = completed ? '✓ Completed' : 'Mark as Complete';
        }
    }

    function updateSidebarProgress() {
        // Update progress indicators in sidebar
        document.querySelectorAll('.nav-item').forEach(item => {
            const articleId = item.dataset.id;
            if (articleId) {
                const completed = isCompleted(articleId);
                item.classList.toggle('nav-item-completed', completed);
            }
        });
    }

    // ========== Expose global ==========
    window.loadArticle = loadArticle;
    window.toggleCheckin = toggleCheckin;

    // ========== Boot ==========
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
