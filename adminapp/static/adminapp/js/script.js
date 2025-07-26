// adminapp/static/adminapp/js/script.js

// Get the table and form elements
const table = document.getElementById('students-table');
const editForm = document.getElementById('edit-student-form');

// Add event listeners for edit and delete buttons
table.addEventListener('click', (e) => {
    if (e.target.classList.contains('edit-btn')) {
        const studentId = e.target.dataset.studentId;
        // Get the student data from the server using AJAX
        fetch(`/students/${studentId}/`)
            .then(response => response.json())
            .then(data => {
                // Fill the form with the student data
                editForm.elements['id'].value = data.id;
                editForm.elements['name'].value = data.name;
                editForm.elements['roll_number'].value = data.roll_number;
                // Show the form
                editForm.style.display = 'block';
            })
            .catch(error => console.error('Error fetching student data:', error));
    } else if (e.target.classList.contains('delete-btn')) {
        const studentId = e.target.dataset.studentId;
        // Send a DELETE request to the server using AJAX
        fetch(`/students/${studentId}/`, {
            method: 'DELETE',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.json())
            .then(data => {
                // Remove the student from the table
                const row = table.querySelector(`tr[data-student-id="${studentId}"]`);
                row.remove();
            })
            .catch(error => console.error('Error deleting student:', error));
    }
});

// Add an event listener for the edit form submission
editForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const studentId = editForm.elements['id'].value;
    const name = editForm.elements['name'].value;
    const rollNumber = editForm.elements['roll_number'].value;
    // Send a PATCH request to the server using AJAX
    fetch(`/students/${studentId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, roll_number: rollNumber })
    })
        .then(response => response.json())
        .then(data => {
            // Update the student data in the table
            const row = table.querySelector(`tr[data-student-id="${studentId}"]`);
            row.cells[0].textContent = data.name;
            row.cells[1].textContent = data.roll_number;
            // Hide the form
            editForm.style.display = 'none';
        })
        .catch(error => console.error('Error updating student:', error));
});