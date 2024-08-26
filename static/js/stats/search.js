order_type = document.getElementById('order-type');
sort_buttons = document.querySelectorAll('.sort-btn');
toggle_info = {};

// ascending icon: <i class="fas fa-sort-down"></i>
// descending icon: <i class="fas fa-sort-up"></i>

for (let i = 0; i < sort_buttons.length; i++) {
  identifier = sort_buttons[i].id;
  toggle_info[identifier] = 'asc'; // Initial sort order
  sort_buttons[i].innerHTML = '<i class="fas fa-sort-down"></i>';
}

document.querySelectorAll('.sort-btn').forEach(item => {
  item.addEventListener('click', event => {
    identifier = item.id;

    // Update sort order info
    if (toggle_info[identifier] === 'desc') {
      toggle_info[identifier] = 'asc';
      order_type.value = 'asc'; // Update hidden input
      item.innerHTML = '<i class="fas fa-sort-down"></i>';
    } else {
      toggle_info[identifier] = 'desc';
      order_type.value = 'desc';
      item.innerHTML = '<i class="fas fa-sort-up"></i>';
    }

    // Implement your sorting logic based on toggle_info[identifier] and identifier
    console.log("Sorted order changed to: " + order_type.value + " for " + identifier);
  });
});
