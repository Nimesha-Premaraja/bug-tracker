/**
 * PDF Export Modal and Export Handler
 * Handles user interaction for exporting bugs to PDF
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    const exportPdfModal = document.getElementById('exportPdfModal');
    const cancelExportBtn = document.getElementById('cancelExportBtn');
    const confirmExportBtn = document.getElementById('confirmExportBtn');
    const modalClose = document.querySelector('.modal-close');
    const loadingIndicator = document.getElementById('loading-indicator');
    const exportWarning = document.getElementById('export-warning');
    const warningText = document.getElementById('warning-text');
    
    const currentPageRadio = document.querySelector('input[value="current-page"]');
    const allResultsRadio = document.querySelector('input[value="all-results"]');
    
    const currentPageCount = document.getElementById('current-page-count');
    const allResultsCount = document.getElementById('all-results-count');
    
    // Update counts on page load
    updateCounts();
    
    // Export button click handler
    exportPdfBtn.addEventListener('click', openModal);
    
    // Cancel button handler
    cancelExportBtn.addEventListener('click', closeModal);
    
    // Close button handler
    modalClose.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === exportPdfModal) {
            closeModal();
        }
    });
    
    // Confirm button handler
    confirmExportBtn.addEventListener('click', submitExport);
    
    // Radio button change handlers
    currentPageRadio.addEventListener('change', updateWarnings);
    allResultsRadio.addEventListener('change', updateWarnings);
    
    /**
     * Open the export modal
     */
    function openModal() {
        exportPdfModal.style.display = 'block';
        loadingIndicator.style.display = 'none';
        updateCounts();
    }
    
    /**
     * Close the export modal
     */
    function closeModal() {
        exportPdfModal.style.display = 'none';
        loadingIndicator.style.display = 'none';
    }
    
    /**
     * Update bug counts for both export options
     */
    function updateCounts() {
        if (!window.bugsFilterData) return;
        
        const currentPageCount_val = window.bugsFilterData.current_page_items;
        const totalItems = window.bugsFilterData.total_items;
        
        currentPageCount.innerHTML = `(${currentPageCount_val} bug${currentPageCount_val !== 1 ? 's' : ''} on this page)`;
        allResultsCount.innerHTML = `(${totalItems} bug${totalItems !== 1 ? 's' : ''} matching filters)`;
    }
    
    /**
     * Update warning messages based on selected option
     */
    function updateWarnings() {
        const selectedScope = document.querySelector('input[name="export-scope"]:checked').value;
        const totalItems = window.bugsFilterData.total_items;
        const warningThreshold = 400;
        
        if (selectedScope === 'all-results' && totalItems > warningThreshold) {
            exportWarning.style.display = 'block';
            warningText.textContent = `Exporting ${totalItems} bugs. This may take a moment.`;
        } else {
            exportWarning.style.display = 'none';
        }
    }
    
    /**
     * Submit the export request
     */
    function submitExport() {
        const selectedScope = document.querySelector('input[name="export-scope"]:checked').value;
        const exportAll = selectedScope === 'all-results';
        
        // Show loading indicator
        showLoadingState();
        
        // Prepare form data with current filters
        const formData = new FormData();
        formData.append('search', window.bugsFilterData.search);
        formData.append('status', window.bugsFilterData.status);
        formData.append('priority', window.bugsFilterData.priority);
        formData.append('assignee_id', window.bugsFilterData.assignee_id);
        formData.append('sort', 'created_at');
        formData.append('order', 'desc');
        formData.append('export_all', exportAll ? 'true' : 'false');
        
        // Add page number if exporting current page only
        if (!exportAll) {
            formData.append('page', window.bugsFilterData.page);
        }
        
        // Send request to backend
        fetch('/bugs/export-pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
        })
        .then(blob => {
            // Generate filename with current date
            const date = new Date();
            const dateString = date.toISOString().split('T')[0]; // YYYY-MM-DD
            const filename = `BugReport_${dateString}.pdf`;
            
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            
            // Trigger download
            document.body.appendChild(link);
            link.click();
            
            // Cleanup
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            // Close modal and show success message
            closeModal();
            showSuccessMessage(`PDF exported successfully as ${filename}`);
        })
        .catch(error => {
            console.error('Error:', error);
            closeModal();
            showErrorMessage('Failed to export PDF. Please try again.');
        });
    }
    
    /**
     * Show loading state in modal
     */
    function showLoadingState() {
        loadingIndicator.style.display = 'block';
        confirmExportBtn.disabled = true;
    }
    
    /**
     * Show success message
     */
    function showSuccessMessage(message) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = 'alert alert-success';
        alert.textContent = message;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            z-index: 10000;
            max-width: 400px;
        `;
        
        document.body.appendChild(alert);
        
        // Remove after 3 seconds
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
    
    /**
     * Show error message
     */
    function showErrorMessage(message) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = 'alert alert-error';
        alert.textContent = message;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            z-index: 10000;
            max-width: 400px;
        `;
        
        document.body.appendChild(alert);
        
        // Remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
});
