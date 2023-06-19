$(document).ready(function () {
    const searchField = document.querySelector("#SearchField");

    const tableOutput = document.querySelector('.search-result-list');
    const noResults = document.querySelector('.no-result');
    const tbody = document.querySelector('.search-result-list');


    searchField.addEventListener("keyup", (e) => {
        var key = e.which
        const un_check_keycodes = [9, 13, 16, 17, 18, 19, 20, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 144,]
        if (un_check_keycodes.includes(key)) {

        } else {
            const searchValue = e.target.value;
            noResults.style.display = "block";

            if (searchValue.trim().length > 0) {

                tbody.innerHTML = "";

                fetch("/search-expenses/", {
                    body: JSON.stringify({searchText: searchValue}),
                    method: "POST",
                })
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.length === 0) {
                            // tableOutput.style.display = "none";
                            noResults.style.display = "block";
                            tbody.innerHTML += noResults.innerHTML


                        } else {
                            noResults.style.display = "none";

                            data.forEach((item) => {

                                tbody.innerHTML += `
                            <li>
                                    <a href="/products/${item.slug}/">${item.title_ir}</a>
                            </li>



                            `;


                            });


                        }
                    });
            } else {
                tableOutput.style.display = "none";


            }
        }

    });

});
