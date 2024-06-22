const max_attribute_level = 99;
const max_badge_level = 4;

let attribute_plus_buttons = document.getElementsByClassName('attribute-plus');
let attribute_minus_buttons = document.getElementsByClassName('attribute-minus');
let attribute_values = document.getElementsByClassName('attribute-value');

let badge_plus_buttons = document.getElementsByClassName('badge-plus');
let badge_minus_buttons = document.getElementsByClassName('badge-minus');
let badge_values = document.getElementsByClassName('badge-value');



// TODO: Update the price of the badge based on the level

attribute_plus_buttons = Array.from(attribute_plus_buttons);
attribute_plus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.attribute-value');
        let updated_value = parseInt(closest_input.textContent) + 1;
        if (updated_value <= max_attribute_level) {
            closest_input.textContent = updated_value;
        };
    });
});

attribute_minus_buttons = Array.from(attribute_minus_buttons);
attribute_minus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        // Get the closest input element, and update the value
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.attribute-value');
        let original_value = parseInt(closest_input.getAttribute('data-original'));
        let updated_value = parseInt(closest_input.textContent) - 1;
        // Check if the updated value is greater than the original (starting) value
        if (updated_value >= original_value) {
            closest_input.textContent = updated_value;
        };
    });
});