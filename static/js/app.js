const backToTop = document.querySelector(".back-to-top");

window.addEventListener("scroll", () => {
  if (window.scrollY > 200) {
    document.body.classList.add("scroll-up");
  } else {
    document.body.classList.remove("scroll-up");
  }
});

backToTop.addEventListener("click", () => {
  window.scrollTo(0, 0);
});

const hamburger = document.getElementById("hamburger");
const menu = document.querySelector(".nav");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("open");
  menu.classList.toggle("open");
});

const links = document.querySelectorAll("nav a");

links.forEach(function (link) {
  link.addEventListener("click", function (event) {
    links.forEach(function (link) {
      link.classList.remove("active");
      hamburger.classList.remove("open");
      menu.classList.remove("open");
    });

    link.classList.add("active");
  });
});

const cardNumberInput = document.getElementById("cardnumber");
const cvcInput = document.getElementById("cvc");
const expiryDateInput = document.getElementById("expirydate");
const cardLogoDiv = document.getElementById("cardlogo");

if (cardNumberInput !== null) {
  expiryDateInput.addEventListener("input", (e) => {
    const input = e.target;
    let value = input.value.replace(/\D/g, "");

    const month = value.slice(0, 2);
    if (parseInt(month) > 12) {
      alert("Month cannot be greater than 12");
      value = "";
    }

    if (value.length >= 2 && value.charAt(1) !== "/") {
      value = value.slice(0, 2) + "/" + value.slice(2);
    }

    if (value.length === 3 && input.value.length < input.oldValue.length) {
      value = value.slice(0, 2);
    }

    input.value = value;
    input.oldValue = value;
  });

  cvcInput.addEventListener("input", (e) => {
    const value = e.target.value;
    const formattedValue = formatCardNumber(value);
    e.target.value = formattedValue;
  });
  cardNumberInput.addEventListener("input", (e) => {
    const value = e.target.value;
    const formattedValue = formatCardNumber(value);
    e.target.value = formattedValue;
    updateCardLogo(formattedValue);
  });

  function formatCardNumber(value) {
    const digitsOnly = value.replace(/\D/g, "");
    const formatted = digitsOnly.match(/.{1,4}/g)?.join(" ") || "";
    return formatted;
  }

  function updateCardLogo(value) {
    const cardType = detectCardType(value);
    const imgSrc =
      cardType === "Visa"
        ? "./img/visa-Logo.png"
        : cardType === "Mastercard"
        ? "./img/mastercard-logo.png"
        : "";

    cardLogoDiv.innerHTML = imgSrc ? `<img src="${imgSrc}">` : "";
  }

  function detectCardType(value) {
    const visaRegex = /^4/;
    const mastercardRegex = /^5[1-5]/;
    if (visaRegex.test(value)) {
      return "Visa";
    } else if (mastercardRegex.test(value)) {
      return "Mastercard";
    } else {
      return "";
    }
  }
}

const setupHtml = document.getElementById("set-up-profile");

const mainJournalHtml = document.getElementById("main-journal");
const mainArticlesHtml = document.getElementById("main-articles");
const singleArticlesHtml = document.querySelector(
  "#single-journal.single-article"
);
const sortAll = document.querySelector(".sort-all-option");
const eventsHtml = document.querySelector(".events");
const trainingsHtml = document.querySelector(".trainings");

if (setupHtml !== null) {
  // Image upload
  const imageUpload = document.querySelector("#image-upload");
  const imageContainer = document.querySelector(".add-image");
  const removeIcon = document.querySelector(".remove-image");

  imageUpload.addEventListener("change", (e) => {
    const file = imageUpload.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      let imageData = event.target.result;
      const image = document.createElement("img");
      image.src = imageData;

      image.classList.add("uploaded-image");
      const uploadedImage = imageContainer.querySelector(".uploaded-image");
      if (uploadedImage) {
        uploadedImage.remove();
      }
      imageContainer.appendChild(image);
      removeIcon.style.display = "block";
      emptyImageContainer.classList.add("hide");
      const onClick = () => {
        imageUpload.click();
      };
      image.addEventListener("click", onClick);
      removeIcon.addEventListener("click", () => {
        const uploadedImage = imageContainer.querySelector(".uploaded-image");
        uploadedImage.remove();
        emptyImageContainer.classList.remove("hide");
        removeIcon.style.display = "none";

        image.removeEventListener("click", onClick);
      });
    };
    reader.readAsDataURL(file);
  });

  // Country list

  const countrySelect = document.getElementById("country");

  fetch("https://restcountries.com/v3.1/all")
    .then((response) => response.json())
    .then((data) => {
      const countries = data.map((country) => ({
        name: country.name.common,
        code: country.cca2,
      }));
      countries.sort((a, b) => a.name.localeCompare(b.name));
      countries.forEach((country) => {
        const option = document.createElement("option");
        option.value = country.code;
        option.textContent = country.name;
        countrySelect.appendChild(option);
      });
    });
}
if (mainJournalHtml !== null) {
  sortAll.addEventListener("click", (e) => {
    if (!sortAll.classList.contains("sort-active")) {
      sortAll.classList.add("sort-active");
      sortOptions.forEach((sortOption) => {
        sortOption.classList.remove("sort-active");
      });
    }
  });
  const sortOptions = document.querySelectorAll(".sort-option");
  const journals = document.querySelectorAll(".journals .journal");
  const notFound = document.querySelector(".not-found");

  // Sorting
  const journalSorting = () => {
    const selectedOptions = document.querySelectorAll(
      ".sort-option.sort-active p"
    );
    if (selectedOptions.length === 0) {
      journals.forEach((journal) => {
        journal.classList.remove("hidden");
        sortAll.classList.add("sort-active");
        notFound.style.display = "none";
      });
      return;
    }

    const selectedOptionsText = Array.prototype.map.call(
      selectedOptions,
      (option) => option.textContent.toLowerCase()
    );
    let availableOptionsCount = 0;

    journals.forEach((journal) => {
      const journalHeading = journal
        .querySelector(".journal-head p")
        .textContent.toLowerCase();
      if (
        selectedOptionsText.some((option) => journalHeading.includes(option))
      ) {
        journal.classList.remove("hidden");
        availableOptionsCount++;
      } else {
        journal.classList.add("hidden");
      }
    });
    if (selectedOptions.length > 0 && availableOptionsCount === 0) {
      notFound.style.display = "flex";
    } else {
      notFound.style.display = "none";
    }
  };
  sortOptions.forEach((sortOption) => {
    sortOption.addEventListener("click", () => {
      sortAll.classList.remove("sort-active");
      sortOption.classList.toggle("sort-active");
      journalSorting();
    });
  });

  sortAll.addEventListener("click", () => {
    sortOptions.forEach((option) => {
      option.classList.remove("sort-active");
    });
    journals.forEach((journal) => {
      journal.classList.remove("hidden");
    });
  });

  // Sorting

  // Pagination
  const itemsPerPage = 6;

  function updatePagination() {
    const totalPages = Math.ceil(journals.length / itemsPerPage);
    const pagination = document.querySelector(".pagination");
    pagination.innerHTML = "";

    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > 5) {
      if (currentPage <= 3) {
        endPage = 5;
      } else if (currentPage >= totalPages - 2) {
        startPage = totalPages - 4;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    if (startPage !== 1) {
      pagination.innerHTML += `<p>1</p>`;
      if (startPage > 2) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pagination.innerHTML += `<p class="${
        currentPage === i ? "current-page" : ""
      }">${i}</p>`;
    }

    if (endPage !== totalPages) {
      if (endPage < totalPages - 1) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
      pagination.innerHTML += `<p>${totalPages}</p>`;
    }

    const pageNumbers = pagination.querySelectorAll("p");
    pageNumbers.forEach((pageNumber, index) => {
      pageNumber.addEventListener("click", () => {
        currentPage = startPage + index;
        updatePagination();
        showPage(currentPage);
        notFound.style.display = "none !important";
      });
    });
    notFound.style.display = "none";
  }

  function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = page * itemsPerPage;

    journals.forEach((journal, index) => {
      if (index >= startIndex && index < endIndex) {
        journal.style.display = "flex";
      } else {
        journal.style.display = "none";
      }
    });
  }

  let currentPage = 1;
  showPage(currentPage);
  updatePagination();

  // Pagination
}
if (trainingsHtml !== null) {
  const journals = document.querySelectorAll(".journals .journal");
  // Pagination
  const itemsPerPage = 6;

  function updatePagination() {
    const totalPages = Math.ceil(journals.length / itemsPerPage);
    const pagination = document.querySelector(".pagination");
    pagination.innerHTML = "";

    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > 5) {
      if (currentPage <= 3) {
        endPage = 5;
      } else if (currentPage >= totalPages - 2) {
        startPage = totalPages - 4;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    if (startPage !== 1) {
      pagination.innerHTML += `<p>1</p>`;
      if (startPage > 2) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pagination.innerHTML += `<p class="${
        currentPage === i ? "current-page" : ""
      }">${i}</p>`;
    }

    if (endPage !== totalPages) {
      if (endPage < totalPages - 1) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
      pagination.innerHTML += `<p>${totalPages}</p>`;
    }

    const pageNumbers = pagination.querySelectorAll("p");
    pageNumbers.forEach((pageNumber, index) => {
      pageNumber.addEventListener("click", () => {
        currentPage = startPage + index;
        updatePagination();
        showPage(currentPage);
      });
    });
  }

  function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = page * itemsPerPage;

    journals.forEach((journal, index) => {
      if (index >= startIndex && index < endIndex) {
        journal.style.display = "flex";
      } else {
        journal.style.display = "none";
      }
    });
  }

  let currentPage = 1;
  showPage(currentPage);
  updatePagination();

  // Pagination
}

if (
  mainArticlesHtml !== null &&
  singleArticlesHtml === null &&
  trainingsHtml === null
) {
  sortAll.addEventListener("click", (e) => {
    if (!sortAll.classList.contains("sort-active")) {
      sortAll.classList.add("sort-active");
      sortOptions.forEach((sortOption) => {
        sortOption.classList.remove("sort-active");
      });
    }
  });
  const sortOptions = document.querySelectorAll(".sort-option");
  const journals = document.querySelectorAll(".journals .journal");
  const notFound = document.querySelector(".not-found");

  // Sorting
  const journalSorting = () => {
    const selectedOptions = document.querySelectorAll(
      ".sort-option.sort-active p"
    );
    if (selectedOptions.length === 0) {
      journals.forEach((journal) => {
        journal.classList.remove("hidden");
        sortAll.classList.add("sort-active");
        notFound.style.display = "none";
      });
      return;
    }

    const selectedOptionsText = Array.prototype.map.call(
      selectedOptions,
      (option) => option.textContent.toLowerCase()
    );
    let availableOptionsCount = 0;

    journals.forEach((journal) => {
      const journalHeading = journal
        .querySelector(".access-type div p")
        .textContent.toLowerCase();
      if (
        selectedOptionsText.some((option) => journalHeading.includes(option))
      ) {
        journal.classList.remove("hidden");
        availableOptionsCount++;
      } else {
        journal.classList.add("hidden");
      }
    });
    if (selectedOptions.length > 0 && availableOptionsCount === 0) {
      notFound.style.display = "flex";
    } else {
      notFound.style.display = "none";
    }
  };
  sortOptions.forEach((sortOption) => {
    sortOption.addEventListener("click", () => {
      sortAll.classList.remove("sort-active");
      sortOption.classList.toggle("sort-active");
      journalSorting();
    });
  });

  sortAll.addEventListener("click", () => {
    sortOptions.forEach((option) => {
      option.classList.remove("sort-active");
    });
    journals.forEach((journal) => {
      journal.classList.remove("hidden");
    });
  });

  // Sorting
  // Pagination
  const itemsPerPage = 6;

  function updatePagination() {
    const totalPages = Math.ceil(journals.length / itemsPerPage);
    const pagination = document.querySelector(".pagination");
    pagination.innerHTML = "";

    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > 5) {
      if (currentPage <= 3) {
        endPage = 5;
      } else if (currentPage >= totalPages - 2) {
        startPage = totalPages - 4;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    if (startPage !== 1) {
      pagination.innerHTML += `<p>1</p>`;
      if (startPage > 2) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pagination.innerHTML += `<p class="${
        currentPage === i ? "current-page" : ""
      }">${i}</p>`;
    }

    if (endPage !== totalPages) {
      if (endPage < totalPages - 1) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
      pagination.innerHTML += `<p>${totalPages}</p>`;
    }

    const pageNumbers = pagination.querySelectorAll("p");
    pageNumbers.forEach((pageNumber, index) => {
      pageNumber.addEventListener("click", () => {
        currentPage = startPage + index;
        updatePagination();
        showPage(currentPage);
        notFound.style.display = "none !important";
      });
    });
    notFound.style.display = "none";
  }

  function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = page * itemsPerPage;

    journals.forEach((journal, index) => {
      if (index >= startIndex && index < endIndex) {
        journal.style.display = "flex";
      } else {
        journal.style.display = "none";
      }
    });
  }

  let currentPage = 1;
  showPage(currentPage);
  updatePagination();

  // Pagination
}

if (eventsHtml !== null && trainingsHtml === null) {
  const sortOptions = document.querySelectorAll(".sort-option");
  const journals = document.querySelectorAll(".journals .journal");
  const notFound = document.querySelector(".not-found");

  // Sorting
  const journalSorting = () => {
    const selectedOptions = document.querySelectorAll(
      ".sort-option.sort-active p"
    );
    if (selectedOptions.length === 0) {
      journals.forEach((journal) => {
        journal.classList.remove("hidden");
        sortAll.classList.add("sort-active");
        notFound.style.display = "none !important";
      });
      return;
    }

    const selectedOptionsText = Array.prototype.map.call(
      selectedOptions,
      (option) => option.textContent.toLowerCase()
    );
    let availableOptionsCount = 0;

    journals.forEach((journal) => {
      const journalHeading = journal
        .querySelector(".content h5")
        .textContent.toLowerCase();

      if (
        selectedOptionsText.some((option) => journalHeading.includes(option))
      ) {
        journal.classList.remove("hidden");
        availableOptionsCount++;
      } else {
        journal.classList.add("hidden");
      }
    });
    if (selectedOptions.length > 0 && availableOptionsCount === 0) {
      notFound.style.display = "flex";
    } else {
      notFound.style.display = "none";
    }
  };
  sortOptions.forEach((sortOption) => {
    sortOption.addEventListener("click", () => {
      sortAll.classList.remove("sort-active");
      journalSorting();
    });
  });

  sortAll.addEventListener("click", () => {
    sortOptions.forEach((option) => {
      option.classList.remove("sort-active");
    });
    journals.forEach((journal) => {
      journal.classList.remove("hidden");
      notFound.style.display = "none";
    });
  });

  // Sorting
  // Pagination
  const itemsPerPage = 6;

  function updatePagination() {
    const totalPages = Math.ceil(journals.length / itemsPerPage);
    const pagination = document.querySelector(".pagination");
    pagination.innerHTML = "";

    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > 5) {
      if (currentPage <= 3) {
        endPage = 5;
      } else if (currentPage >= totalPages - 2) {
        startPage = totalPages - 4;
      } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
      }
    }

    if (startPage !== 1) {
      pagination.innerHTML += `<p>1</p>`;
      if (startPage > 2) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pagination.innerHTML += `<p class="${
        currentPage === i ? "current-page" : ""
      }">${i}</p>`;
    }

    if (endPage !== totalPages) {
      if (endPage < totalPages - 1) {
        pagination.innerHTML += `<span class="ellipsis">...</span>`;
      }
      pagination.innerHTML += `<p>${totalPages}</p>`;
    }

    const pageNumbers = pagination.querySelectorAll("p");
    pageNumbers.forEach((pageNumber, index) => {
      pageNumber.addEventListener("click", () => {
        currentPage = startPage + index;
        updatePagination();
        showPage(currentPage);
        notFound.style.display = "none !important";
      });
    });
    notFound.style.display = "none";
  }

  function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = page * itemsPerPage;

    journals.forEach((journal, index) => {
      if (index >= startIndex && index < endIndex) {
        journal.style.display = "flex";
      } else {
        journal.style.display = "none";
      }
    });
  }

  let currentPage = 1;
  showPage(currentPage);
  updatePagination();

  // Pagination
}

let selectedOption;

document.addEventListener("DOMContentLoaded", function () {
  const modalContainer = document.querySelector(".publish-modal-container");
  const modalContent = document.querySelector(".modal-content");
  const publishLink = document.querySelector(".publish");
  const closeModalIcon = document.querySelector(".modal-close");

  publishLink.addEventListener("click", () => {
    if (modalContainer) {
      modalContainer.style.display = "flex";
      modalContent.style.display = "flex";

      if (modalContainer.style.display === "flex") {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "auto";
      }
    }
  });
  closeModalIcon.addEventListener("click", () => {
    modalContainer.style.display = "none";
    document.body.style.overflow = "auto";
  });
  const modalOptions = document.querySelectorAll(".publish-journal");

  modalOptions.forEach((option) => {
    option.addEventListener("click", () => {
      modalOptions.forEach((otherOption) => {
        otherOption.classList.remove("modal-select");
      });

      option.classList.add("modal-select");

      selectedOption = option.querySelector("h6").getAttribute("id");
    });
  });
  
  // sending "pubish" button click to the backend
  const modalBtn = document.getElementById('modal--btn');
  modalBtn.addEventListener('click', ()=>{
    if (selectedOption === 'article'){
      // window.location.href = `${window.location.host}/article/add`;
      // window.location.assign(`/article/add`);
      // window.location = `/article/add`;
      window.location.href = `/article/add`;
    }else if(selectedOption === 'journal'){
      window.location.href = `/journal/add`;
    }else if(selectedOption === 'event'){
      window.location.href = `/event/add`;
    }else{
      alert("Unknown action!")
    }
  });
});
