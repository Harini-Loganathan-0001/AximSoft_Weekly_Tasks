document.addEventListener("DOMContentLoaded", function () {

    const table = document.getElementById("dataTable");

    const menu = document.getElementById("columnMenu");

    const headers = table.querySelectorAll("thead th");

    headers.forEach((header, index) => {

        const li = document.createElement("li");

        li.innerHTML = `
        <div class="form-check">

            <input
                class="form-check-input column-toggle"
                type="checkbox"
                checked
                data-column="${index}"
                id="col${index}">

            <label class="form-check-label" for="col${index}">
                ${header.innerText}
            </label>

        </div>
        `;

        menu.appendChild(li);

    });

    document.querySelectorAll(".column-toggle").forEach(box => {

        box.addEventListener("change", function () {

            const col = this.dataset.column;

            const display = this.checked ? "" : "none";

            table.querySelectorAll("tr").forEach(row => {

                if (row.cells[col]) {

                    row.cells[col].style.display = display;

                }

            });

        });

    });

});