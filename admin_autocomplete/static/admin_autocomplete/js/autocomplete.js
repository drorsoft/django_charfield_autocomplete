'use strict';

document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin autocomplete script loaded');
    
    const searchInput = document.querySelector('#searchbar');
    if (!searchInput) {
        console.log('Search input not found');
        return;
    }
    console.log('Search input found:', searchInput);

    // Create and append the autocomplete container
    const autocompleteContainer = document.createElement('div');
    autocompleteContainer.id = 'admin-autocomplete-results';
    autocompleteContainer.className = 'admin-autocomplete-results';
    searchInput.parentNode.insertBefore(autocompleteContainer, searchInput.nextSibling);
    console.log('Autocomplete container created');

    let currentRequest = null;
    let debounceTimer;

    searchInput.addEventListener('input', function() {
        console.log('Input event triggered');
        const term = this.value.trim();
        console.log('Search term:', term);

        clearTimeout(debounceTimer);
        if (currentRequest) {
            currentRequest.abort();
        }

        if (term.length < 2) {
            autocompleteContainer.innerHTML = '';
            autocompleteContainer.style.display = 'none';
            return;
        }

        debounceTimer = setTimeout(() => {
            // Build the autocomplete URL based on current page URL
            const currentPath = window.location.pathname;
            // Remove trailing slash if exists and add autocomplete/
            const autocompleteUrl = currentPath.replace(/\/$/, '') + '/autocomplete/';
            console.log('Fetching from:', autocompleteUrl);

            fetch(`${autocompleteUrl}?term=${encodeURIComponent(term)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(text => {
                console.log('Raw response:', text);
                if (!text) {
                    console.log('Empty response received');
                    return { results: [] };
                }
                try {
                    return JSON.parse(text);
                } catch (e) {
                    console.error('JSON parse error:', e);
                    console.log('Failed to parse text:', text);
                    return { results: [] };
                }
            })
            .then(data => {
                console.log('Parsed data:', data);
                autocompleteContainer.innerHTML = '';
                
                if (data.results && data.results.length > 0) {
                    data.results.forEach(function(item) {
                        const resultItem = document.createElement('div');
                        resultItem.className = 'autocomplete-item';
                        resultItem.textContent = item.text;
                        resultItem.addEventListener('click', function() {
                            window.location.href = item.url;
                        });
                        autocompleteContainer.appendChild(resultItem);
                    });
                    autocompleteContainer.style.display = 'block';
                } else {
                    autocompleteContainer.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                autocompleteContainer.innerHTML = '';
                autocompleteContainer.style.display = 'none';
            });
        }, 300); // Debounce delay
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!autocompleteContainer.contains(e.target) && e.target !== searchInput) {
            autocompleteContainer.style.display = 'none';
        }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const items = autocompleteContainer.getElementsByClassName('autocomplete-item');
        const selected = autocompleteContainer.querySelector('.selected');
        
        if (items.length === 0) return;
        
        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (!selected) {
                    items[0].classList.add('selected');
                } else {
                    const next = selected.nextElementSibling;
                    if (next) {
                        selected.classList.remove('selected');
                        next.classList.add('selected');
                    }
                }
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                if (selected) {
                    const prev = selected.previousElementSibling;
                    selected.classList.remove('selected');
                    if (prev) {
                        prev.classList.add('selected');
                    }
                }
                break;
                
            case 'Enter':
                if (selected) {
                    e.preventDefault();
                    window.location.href = selected.dataset.url;
                }
                break;
                
            case 'Escape':
                autocompleteContainer.style.display = 'none';
                break;
        }
    });
});
