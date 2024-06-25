// Use 'https://cdn.skypack.dev/' + 'npm package name' + '@version its optional'
import { generate, display } from "https://cdn.skypack.dev/facesjs@3.8.1";
const face_status = document.getElementById("face-status");
const randomize_button = document.getElementById("randomize");
const save_button = document.getElementById("save");
const player_face = document.getElementById("player-appearance");

// Generation function
const generateFace = (overrides) => {
    // Create overrides if they exist
    let face = undefined;
    if (overrides) {
        const race = document.getElementById("race").value;
        const skin = document.getElementById("skin").value;
        const body = document.getElementById("body").value;
        const ear = document.getElementById("ear").value;
        const eye = document.getElementById("eye").value;
        const eyebrow = document.getElementById("eyebrow").value;
        const facial_hair = document.getElementById("facialHair").value;
        const hair = document.getElementById("hair").value;
        const hair_color = document.getElementById("hairColor").value;
        const head = document.getElementById("head").value;
        const mouth = document.getElementById("mouth").value;
        const nose = document.getElementById("nose").value;
        face = generate({
            gender: "male",
            race: race,
            fatness: 0.5,
            accessories: {
                id: "none",
            },
            glasses: {
                id: "none",
            },
            jersey: {
                id: "jersey4",
            },
            body: {
                id: body,
                color: skin,
                size: 1,
            },
            ear: {
                id: ear,
            },
            eye: {
                id: eye,
            },
            eyebrow: {
                id: eyebrow,
                angle: 20,
            },
            facialHair: {
                id: facial_hair,
                color: hair_color,
            },
            hair: {
                id: hair,
                color: hair_color,
            },
            head: {
                id: head,
            },
            mouth: {
                id: mouth,
            },
            nose: {
                id: nose,
                size: 1,
            },
            smileLine: {
                id: "none",
                size: 2,
            },
        });
    } else {
        face = generate({gender: "male", jersey: {id: "jersey4"}});
    }
    // Display the generated face
    display(player_face, face);
};

// Option selections
const svg_selects = document.querySelectorAll(".svg-select");
svg_selects.forEach((select) => {
    select.addEventListener("change", () => {
        generateFace();
    });
});

// Random face generation
randomize_button.addEventListener("click", () => {
    generateFace(false);
});

// Saving of face generations
save_button.addEventListener("click", () => {
    const edit_appearance_url = "{% url 'edit_appearance' player.id %}";
    htmx.ajax(
        'POST', 
        edit_appearance_url, 
        {
            target: '#player-appearance',
            swap: 'innerHTML',
            headers: { 
                'X-CSRFToken': '{{ csrf_token }}'
            },
            values: { face: document.getElementById("player-appearance").innerHTML }
        }
    );
});