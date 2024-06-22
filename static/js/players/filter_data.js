// Filter data for player attributes and badges
const shown_attributes = document.querySelectorAll('input[name="shown_attributes"]');
const shown_badges = document.querySelectorAll('input[name="shown_badges"]');
const attribute_list = document.getElementById('attribute_list');
const badge_list = document.getElementById('badge_list');

const hide_map = {
    'show_finishing_attributes': 'Finishing',
    'show_shooting_attributes': 'Shooting',
    'show_playmaking_attributes': 'Playmaking',
    'show_defensive_attributes': 'Defensive',
    'show_physical_attributes': 'Physical',
    'show_finishing_badges': 'Finishing',
    'show_shooting_badges': 'Shooting',
    'show_playmaking_badges': 'Playmaking',
    'show_defensive_badges': 'Defensive',
}

shown_attributes.forEach((element) => {
    element.addEventListener('change', () => {
        console.log(element);
        const category = element.id;
        const data_category = hide_map[category];
        for (i = 0; i < attribute_list.children.length; i++) {
            const attribute = attribute_list.children[i];
            if (data_category) {
                if (attribute.dataset.category !== data_category) {
                    console.log(attribute.dataset.category);
                    attribute.style.display = 'none';
                } else {
                    attribute.style.display = 'block';
                }
            } else {
                attribute.style.display = 'block';
            }
        }
    });
});

shown_badges.forEach((element) => {
    element.addEventListener('change', () => {
        const category = element.id;
        const data_category = hide_map[category];
        for (i = 0; i < badge_list.children.length; i++) {
            const badge = badge_list.children[i];
            if (data_category) {
                if (badge.dataset.category !== data_category) {
                    badge.style.display = 'none';
                } else {
                    badge.style.display = 'block';
                }
            } else {
                badge.style.display = 'block';
            }
        }
    });
});