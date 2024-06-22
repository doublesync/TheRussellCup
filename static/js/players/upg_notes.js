const player_id = document.getElementById('player_id').value;
const upgrade_notes_status = document.getElementById('upgrade_notes_status');
const submit_upgrade_notes = document.getElementById('submit_upgrade_notes');

window.onload = function() {
    const existing_upgrade_notes = window.localStorage.getItem(`${player_id}_upgrade_notes`);
    let upgrade_notes = document.getElementById('upgrade_notes');
    if (existing_upgrade_notes !== null) {
        upgrade_notes.value = existing_upgrade_notes;
        upgrade_notes_status.innerHTML = 'Upgrade notes loaded!';
    }
}

submit_upgrade_notes.addEventListener('click', function() {
    upgrade_notes = document.getElementById('upgrade_notes').value;
    if (upgrade_notes) {
        window.localStorage.setItem(`${player_id}_upgrade_notes`, upgrade_notes);
        upgrade_notes_status.innerHTML = 'Upgrade notes saved!';
    } else {
        upgrade_notes_status.innerHTML = 'Please enter upgrade notes!';
    }
});
