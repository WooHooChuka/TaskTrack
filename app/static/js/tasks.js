document.addEventListener('DOMContentLoaded', function() {
  // Task filtering
  const statusFilter = document.getElementById('status-filter');
  const priorityFilter = document.getElementById('priority-filter');
  const applyFiltersBtn = document.getElementById('apply-filters');
  
  applyFiltersBtn.addEventListener('click', function() {
    const status = statusFilter.value;
    const priority = priorityFilter.value;
    
    // Build the query string
    let queryParams = [];
    if (status) queryParams.push(`status=${status}`);
    if (priority) queryParams.push(`priority=${priority}`);
    
    const queryString = queryParams.length > 0 ? `?${queryParams.join('&')}` : '';
    
    // Redirect to the filtered view
    window.location.href = `/tasks${queryString}`;
  });
  
  // Delete task functionality
  const deleteButtons = document.querySelectorAll('.delete-task');
  const deleteModal = document.getElementById('delete-modal');
  const confirmDeleteBtn = document.getElementById('confirm-delete');
  const cancelDeleteBtn = document.getElementById('cancel-delete');
  let taskToDelete = null;
  
  deleteButtons.forEach(button => {
    button.addEventListener('click', function() {
      taskToDelete = this.getAttribute('data-task-id');
      deleteModal.style.display = 'flex';
    });
  });
  
  cancelDeleteBtn.addEventListener('click', function() {
    deleteModal.style.display = 'none';
    taskToDelete = null;
  });
  
  confirmDeleteBtn.addEventListener('click', function() {
    if (taskToDelete) {
      // Create a form to submit the delete request
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = `/tasks/${taskToDelete}/delete`;
      document.body.appendChild(form);
      form.submit();
    }
  });
  
  // Close modal when clicking outside
  window.addEventListener('click', function(event) {
    if (event.target === deleteModal) {
      deleteModal.style.display = 'none';
      taskToDelete = null;
    }
  });
}); 