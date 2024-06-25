const max_attribute_level = 99;
const max_badge_level = 4;
const max_tendency_level = 100;

let attribute_plus_buttons = document.getElementsByClassName('attribute-plus');
let attribute_minus_buttons = document.getElementsByClassName('attribute-minus');
let attribute_values = document.getElementsByClassName('attribute-value');

let badge_plus_buttons = document.getElementsByClassName('badge-plus');
let badge_minus_buttons = document.getElementsByClassName('badge-minus');
let badge_values = document.getElementsByClassName('badge-value');

let tendency_plus_buttons = document.getElementsByClassName('tendency-plus');
let tendency_minus_buttons = document.getElementsByClassName('tendency-minus');
let tendency_values = document.getElementsByClassName('tendency-value');


attribute_plus_buttons = Array.from(attribute_plus_buttons);
attribute_plus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.attribute-value');
        let updated_value = parseInt(closest_input.value) + 1;
        if (updated_value <= max_attribute_level) {
            closest_input.value = updated_value;
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
        let updated_value = parseInt(closest_input.value) - 1;
        // Check if the updated value is greater than the original (starting) value
        if (updated_value >= original_value) {
            closest_input.value = updated_value;
        };
    });
});

badge_plus_buttons = Array.from(badge_plus_buttons);
badge_plus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.badge-value');
        let updated_value = parseInt(closest_input.value) + 1;
        if (updated_value <= max_badge_level) {
            closest_input.value = updated_value;
        };
    });
});

badge_minus_buttons = Array.from(badge_minus_buttons);
badge_minus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.badge-value');
        let original_value = parseInt(closest_input.getAttribute('data-original'));
        let updated_value = parseInt(closest_input.value) - 1;
        if (updated_value >= original_value) {
            closest_input.value = updated_value;
        };
    });
});

tendency_plus_buttons = Array.from(tendency_plus_buttons);
tendency_plus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.tendency-value');
        let updated_value = parseInt(closest_input.value) + 1;
        if (updated_value <= max_tendency_level) {
            closest_input.value = updated_value;
        };
    });
});

tendency_minus_buttons = Array.from(tendency_minus_buttons);
tendency_minus_buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        let root_div = event.target.closest('div');
        let closest_input = root_div.querySelector('.tendency-value');
        let original_value = parseInt(closest_input.getAttribute('data-original'));
        let updated_value = parseInt(closest_input.value) - 1;
        if (updated_value >= original_value) {
            closest_input.value = updated_value;
        };
    });
});