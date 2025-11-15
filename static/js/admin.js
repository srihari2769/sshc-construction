// Flash Message Close
const flashCloseButtons = document.querySelectorAll('.flash-close');
flashCloseButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.style.animation = 'slideOut 0.3s';
        setTimeout(() => {
            button.parentElement.remove();
        }, 300);
    });
});

// Auto-hide flash messages after 5 seconds
const flashMessages = document.querySelectorAll('.flash-message');
flashMessages.forEach(message => {
    setTimeout(() => {
        message.style.animation = 'slideOut 0.3s';
        setTimeout(() => {
            message.remove();
        }, 300);
    }, 5000);
});

// Delete Item Function
function deleteItem(type, id) {
    if (confirm(`Are you sure you want to delete this ${type}?`)) {
        fetch(`/admin/${type}s/delete/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error deleting item: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting item');
        });
    }
}

// Show Notification
function showNotification(message, type = 'success') {
    const flashContainer = document.querySelector('.flash-container') || createFlashContainer();
    
    const flash = document.createElement('div');
    flash.className = `flash-message flash-${type}`;
    flash.innerHTML = `
        <span>${message}</span>
        <button class="flash-close">&times;</button>
    `;
    
    flashContainer.appendChild(flash);
    
    // Add close functionality
    const closeBtn = flash.querySelector('.flash-close');
    closeBtn.addEventListener('click', () => {
        flash.style.animation = 'slideOut 0.3s';
        setTimeout(() => flash.remove(), 300);
    });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        flash.style.animation = 'slideOut 0.3s';
        setTimeout(() => flash.remove(), 300);
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-container';
    document.body.appendChild(container);
    return container;
}

// Remove Media Function
function removeMedia(mediaId) {
    if (confirm('Are you sure you want to delete this media file?')) {
        fetch(`/admin/media/delete/${mediaId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error deleting media: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting media');
        });
    }
}

// Form Validation
const adminForms = document.querySelectorAll('.admin-form');
adminForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = 'var(--admin-danger)';
            } else {
                field.style.borderColor = '#ddd';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Please fill in all required fields', 'error');
        }
    });
});

// File Input Preview
const fileInputs = document.querySelectorAll('input[type="file"]');
fileInputs.forEach(input => {
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                // Create preview if it doesn't exist
                let preview = input.parentElement.querySelector('.file-preview');
                if (!preview) {
                    preview = document.createElement('div');
                    preview.className = 'file-preview';
                    preview.style.marginTop = '10px';
                    input.parentElement.appendChild(preview);
                }
                
                if (file.type.startsWith('image/')) {
                    preview.innerHTML = `<img src="${e.target.result}" style="max-width: 200px; border-radius: 5px;">`;
                } else {
                    preview.innerHTML = `<p>File selected: ${file.name}</p>`;
                }
            };
            reader.readAsDataURL(file);
        }
    });
});

// Confirm Navigation Away from Unsaved Changes
let formChanged = false;

const formInputs = document.querySelectorAll('.admin-form input, .admin-form textarea, .admin-form select');
formInputs.forEach(input => {
    input.addEventListener('change', () => {
        formChanged = true;
    });
});

window.addEventListener('beforeunload', (e) => {
    if (formChanged) {
        e.preventDefault();
        e.returnValue = '';
    }
});

adminForms.forEach(form => {
    form.addEventListener('submit', () => {
        formChanged = false;
    });
});

// Data Table Sorting
const tables = document.querySelectorAll('.data-table');
tables.forEach(table => {
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => {
            sortTable(table, index);
        });
    });
});

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        return aText.localeCompare(bText, undefined, { numeric: true });
    });
    
    // Toggle sort direction
    if (table.dataset.sortColumn === columnIndex.toString() && table.dataset.sortDirection === 'asc') {
        sortedRows.reverse();
        table.dataset.sortDirection = 'desc';
    } else {
        table.dataset.sortDirection = 'asc';
    }
    
    table.dataset.sortColumn = columnIndex;
    
    // Clear tbody and append sorted rows
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

// Search Functionality
const searchInputs = document.querySelectorAll('.search-input');
searchInputs.forEach(input => {
    input.addEventListener('keyup', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const table = input.closest('.table-responsive').querySelector('.data-table');
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .data-table th {
        position: relative;
        user-select: none;
    }
    
    .data-table th:hover {
        background-color: #1a252f;
    }
`;
document.head.appendChild(style);
