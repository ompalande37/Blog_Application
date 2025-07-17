// AJAX functionality for the blog application
class BlogAJAX {
    constructor() {
        this.baseURL = '/api/';
        this.token = localStorage.getItem('access_token');
        this.setupEventListeners();
    }

    // Setup all event listeners
    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Like functionality
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('like-btn')) {
                this.handleLike(e);
            }
        });

        // Comment form submission
        document.addEventListener('submit', (e) => {
            if (e.target.classList.contains('comment-form')) {
                e.preventDefault();
                this.handleComment(e);
            }
        });

        // Search functionality
        const searchForm = document.getElementById('search-form');
        if (searchForm) {
            console.log('Search form found');
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSearch(e);
            });
        } else {
            console.log('Search form not found');
        }

        // Login form
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            console.log('Login form found');
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin(e);
            });
        } else {
            console.log('Login form not found');
        }

        // Register form
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            console.log('Register form found');
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister(e);
            });
        } else {
            console.log('Register form not found');
        }
    }

    // Set authentication token
    setToken(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    // Get authentication headers
    getAuthHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // Handle like/unlike posts
    async handleLike(event) {
        const button = event.target;
        const postId = button.dataset.postId;
        const likeCount = button.querySelector('.like-count');
        
        try {
            const response = await fetch(`${this.baseURL}posts/${postId}/like/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
            });

            if (response.ok) {
                const data = await response.json();
                const isLiked = data.liked;
                
                // Update button appearance
                if (isLiked) {
                    button.classList.add('liked');
                    button.innerHTML = '<i class="fas fa-heart"></i> <span class="like-count">' + data.likes_count + '</span>';
                } else {
                    button.classList.remove('liked');
                    button.innerHTML = '<i class="far fa-heart"></i> <span class="like-count">' + data.likes_count + '</span>';
                }
                
                // Show success message
                this.showMessage('Post ' + (isLiked ? 'liked' : 'unliked') + ' successfully!', 'success');
            } else if (response.status === 401) {
                this.showMessage('Please login to like posts', 'error');
            } else {
                this.showMessage('Error processing like', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showMessage('Network error occurred', 'error');
        }
    }

    // Handle comment submission
    async handleComment(event) {
        const form = event.target;
        const postId = form.dataset.postId;
        const content = form.querySelector('textarea[name="content"]').value;
        const commentsContainer = document.querySelector('.comments-container');
        
        if (!content.trim()) {
            this.showMessage('Please enter a comment', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}posts/${postId}/add_comment/`, {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify({ content: content })
            });

            if (response.ok) {
                const data = await response.json();
                
                // Add new comment to the page
                const commentHTML = this.createCommentHTML(data);
                commentsContainer.insertAdjacentHTML('afterbegin', commentHTML);
                
                // Clear form
                form.querySelector('textarea[name="content"]').value = '';
                
                // Update comment count
                const commentCount = document.querySelector('.comment-count');
                if (commentCount) {
                    const currentCount = parseInt(commentCount.textContent) || 0;
                    commentCount.textContent = currentCount + 1;
                }
                
                this.showMessage('Comment added successfully!', 'success');
            } else if (response.status === 401) {
                this.showMessage('Please login to comment', 'error');
            } else {
                this.showMessage('Error adding comment', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showMessage('Network error occurred', 'error');
        }
    }

    // Create comment HTML
    createCommentHTML(comment) {
        return `
            <div class="comment" data-comment-id="${comment.id}">
                <div class="comment-header">
                    <strong>${comment.author_name}</strong>
                    <small>${new Date(comment.created_at).toLocaleDateString()}</small>
                </div>
                <div class="comment-content">
                    ${comment.content}
                </div>
            </div>
        `;
    }

    // Handle search
    async handleSearch(event) {
        const form = event.target;
        const searchInput = form.querySelector('input[name="search"]');
        const query = searchInput.value.trim();
        
        if (!query) return;

        try {
            const response = await fetch(`${this.baseURL}posts/?search=${encodeURIComponent(query)}`);
            
            if (response.ok) {
                const data = await response.json();
                this.updateSearchResults(data.results);
            }
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    // Update search results
    updateSearchResults(posts) {
        const resultsContainer = document.getElementById('search-results');
        if (!resultsContainer) return;

        if (posts.length === 0) {
            resultsContainer.innerHTML = '<p>No posts found matching your search.</p>';
            return;
        }

        const postsHTML = posts.map(post => `
            <div class="search-result-item">
                <h4><a href="/post/${post.slug}/">${post.title}</a></h4>
                <p>${post.excerpt}</p>
                <small>By ${post.author_name} on ${new Date(post.timestamp).toLocaleDateString()}</small>
            </div>
        `).join('');

        resultsContainer.innerHTML = postsHTML;
    }

    // Handle user login
    async handleLogin(event) {
        console.log('Login form submitted');
        const form = event.target;
        const formData = new FormData(form);
        const data = {
            username: formData.get('username') || document.getElementById('id_username')?.value,
            password: formData.get('password') || document.getElementById('id_password')?.value
        };

        console.log('Login data:', data);

        try {
            // Try AJAX first
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            console.log('Login response status:', response.status);

            if (response.ok) {
                const result = await response.json();
                console.log('Login successful:', result);
                this.setToken(result.access);
                this.showMessage('Login successful!', 'success');
                
                // Redirect to blog page
                setTimeout(() => {
                    window.location.href = '/blog/';
                }, 1000);
            } else {
                // Fallback to regular form submission
                console.log('AJAX login failed, trying regular form submission');
                form.submit();
            }
        } catch (error) {
            console.error('Login error:', error);
            // Fallback to regular form submission
            form.submit();
        }
    }

    // Handle user registration
    async handleRegister(event) {
        console.log('Registration form submitted');
        const form = event.target;
        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            first_name: formData.get('first_name'),
            last_name: formData.get('last_name')
        };

        console.log('Registration data:', data);

        try {
            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            console.log('Registration response status:', response.status);

            if (response.ok) {
                const result = await response.json();
                console.log('Registration successful:', result);
                this.setToken(result.access);
                this.showMessage('Registration successful!', 'success');
                
                // Redirect to homepage
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                const error = await response.json();
                console.log('Registration error:', error);
                this.showMessage(error.error || 'Registration failed', 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showMessage('Network error occurred', 'error');
        }
    }

    // Show message to user
    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show`;
        messageDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(messageDiv, container.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }

    // Load more posts (pagination)
    async loadMorePosts(page = 1) {
        try {
            const response = await fetch(`${this.baseURL}posts/?page=${page}`);
            
            if (response.ok) {
                const data = await response.json();
                this.appendPosts(data.results);
                
                // Update pagination
                if (data.next) {
                    this.setupLoadMoreButton(data.next);
                }
            }
        } catch (error) {
            console.error('Load more error:', error);
        }
    }

    // Append posts to the page
    appendPosts(posts) {
        const postsContainer = document.querySelector('.posts-container');
        if (!postsContainer) return;

        posts.forEach(post => {
            const postHTML = this.createPostHTML(post);
            postsContainer.insertAdjacentHTML('beforeend', postHTML);
        });
    }

    // Create post HTML
    createPostHTML(post) {
        return `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${post.title}</h5>
                        <p class="card-text">${post.excerpt}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">By ${post.author_name}</small>
                            <a href="/post/${post.slug}/" class="btn btn-primary btn-sm">Read More</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Setup load more button
    setupLoadMoreButton(nextUrl) {
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn) {
            loadMoreBtn.style.display = 'block';
            loadMoreBtn.onclick = () => {
                const page = new URL(nextUrl).searchParams.get('page');
                this.loadMorePosts(page);
            };
        }
    }
}

// Initialize AJAX functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.blogAJAX = new BlogAJAX();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlogAJAX;
} 