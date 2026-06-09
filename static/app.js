(function () {
    const STORAGE_KEY = "surakshit_saved_scenarios";

    const imageInput = document.getElementById("scenarioImage");
    const previewImage = document.getElementById("previewImage");
    const previewText = document.getElementById("previewText");
    const scenarioInput = document.getElementById("scenario");
    const pedestrianCheckbox = document.querySelector("input[value='pedestrian_present']");
    const autoPedestrianBtn = document.getElementById("autoPedestrianBtn");
    const clearBtn = document.getElementById("clearBtn");
    const saveBoardBtn = document.getElementById("saveBoardBtn");
    const historyList = document.getElementById("historyList");
    const historyCount = document.getElementById("historyCount");
    const savedCountRight = document.getElementById("savedCountRight");

    function getSavedItems() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                return [];
            }
            const parsed = JSON.parse(raw);
            return Array.isArray(parsed) ? parsed : [];
        } catch (_error) {
            return [];
        }
    }

    function setSavedItems(items) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    }

    function renderSavedItems() {
        const items = getSavedItems();
        historyList.innerHTML = "";

        items.slice(0, 10).forEach((item) => {
            const li = document.createElement("li");
            li.textContent = `${item.category} (${item.score.toFixed(1)}) - ${item.scenario}`;
            historyList.appendChild(li);
        });

        const countText = `${items.length} saved`;
        historyCount.textContent = countText;
        savedCountRight.textContent = countText;
    }

    function setPreviewFromFile(file) {
        if (!file) {
            previewImage.style.display = "none";
            previewImage.removeAttribute("src");
            previewText.style.display = "block";
            previewText.textContent = "No image uploaded";
            return;
        }

        const reader = new FileReader();
        reader.onload = (event) => {
            previewImage.src = event.target.result;
            previewImage.style.display = "block";
            previewText.style.display = "none";
        };
        reader.readAsDataURL(file);
    }

    imageInput.addEventListener("change", () => {
        const file = imageInput.files && imageInput.files[0] ? imageInput.files[0] : null;
        setPreviewFromFile(file);
    });

    autoPedestrianBtn.addEventListener("click", () => {
        const text = scenarioInput.value.toLowerCase();
        const words = ["child", "children", "student", "students", "pedestrian", "walking", "crossing"];
        const hasPedestrianSignal = words.some((word) => text.includes(word));
        pedestrianCheckbox.checked = hasPedestrianSignal;
    });

    clearBtn.addEventListener("click", () => {
        document.getElementById("riskForm").reset();
        setPreviewFromFile(null);
        window.location.href = "/";
    });

    saveBoardBtn.addEventListener("click", () => {
        const scenario = scenarioInput.value.trim() || "Untitled scenario";
        const existing = getSavedItems();

        const record = {
            scenario: scenario.length > 70 ? `${scenario.slice(0, 70)}...` : scenario,
            score: Number(window.currentResult.score || 0),
            category: window.currentResult.category || "No risk",
            savedAt: new Date().toISOString(),
        };

        const updated = [record, ...existing].slice(0, 50);
        setSavedItems(updated);
        renderSavedItems();
    });

    renderSavedItems();
})();
