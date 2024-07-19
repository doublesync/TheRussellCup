order_type = document.getElementById('order-type');
sort_buttons = document.querySelectorAll('.sort-btn');
toggle_info = {};

for (let i = 0; i < sort_buttons.length; i++) {
    identifier = sort_buttons[i].id;
    toggle_info[identifier] = 'desc';
}

document.querySelectorAll('.sort-btn').forEach(item => {
    item.addEventListener('click', event => {
        identifier = item.id;
        if (toggle_info[identifier] == 'desc') {
            toggle_info[identifier] = 'asc';
            order_type.value = 'asc';
        } else {
            toggle_info[identifier] = 'desc';
            order_type.value = 'desc';
        }
        console.log("Sorted order changed to: " + order_type.value);
    });
});