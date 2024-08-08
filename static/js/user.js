const userDashboard = document.getElementById("user-dashboard");

if (userDashboard !== null) {
  const awardsTab = document.querySelector(".user-body");
  const sortButtons = document.querySelectorAll(".sort-option");
  const sections = document.querySelectorAll(".user-sections section");
  const aboutUser = document.querySelector(".user-info-detail");
  const editProfile = document.querySelector("div.profile-edit");
  const editBtn = document.querySelector(".edit-profile");
  sortButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const activeSection = button.textContent
        .toLowerCase()
        .trim()
        .split(" ")
        .join("");
      sections.forEach((section) => {
        if (section.classList.contains(activeSection)) {
          if (activeSection === "membership") {
            awardsTab.style.display = "none";
          } else {
            awardsTab.style.display = "flex";
          }
          if (activeSection === "profile") {
            aboutUser.style.display = "flex";
            editProfile.classList.toggle("hide");
          }
          section.style.display = "flex";
          section.classList.add("active-section");
        } else {
          section.style.display = "none";
          section.classList.remove("active-section");
        }
      });
      button.classList.add("sort-active");
      sortButtons.forEach((otherButton) => {
        if (otherButton !== button) {
          otherButton.classList.remove("sort-active");
        }
      });
    });
  });
  editBtn.addEventListener("click", () => {
    aboutUser.style.display = "none";
    editProfile.classList.toggle("hide");
  });
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
        option.style.width = "100%";

        countrySelect.appendChild(option);
      });
    });

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
}

const addNewJournalPage = document.getElementById("addNewJournal");
const addNewArticlePage = document.getElementById("addNewArticle");
const addNewEventPage = document.getElementById("addNewEvent");
// if (addNewJournalPage !== null) {
//   document.addEventListener("DOMContentLoaded", function () {
//     const fullJournal = new Quill("#full-text-editor", {
//       modules: {
//         toolbar: [
//           ["bold", "italic", "underline"],
//           ["link", "blockquote", "image"],
//           [{ list: "ordered" }, { list: "bullet" }],
//           [{ color: [] }, { background: [] }],
//         ],
//       },
//       theme: "snow",
//     });
//     const fullAbstract = new Quill("#full-abstract-editor", {
//       modules: {
//         toolbar: [
//           ["bold", "italic", "underline"],
//           ["link", "blockquote", "image"],
//           [{ list: "ordered" }, { list: "bullet" }],
//           [{ color: [] }, { background: [] }],
//         ],
//       },
//       theme: "snow",
//     });
//     const form = document.getElementById("journalForm");
//     form.addEventListener("submit", function (event) {
//       if (fullJournal.getText().trim() === "") {
//         alert("Full journal content cannot be empty!");
//         event.preventDefault();
//         return;
//       }

//       if (fullAbstract.getText().trim() === "") {
//         alert("Abstract content cannot be empty!");
//         event.preventDefault();
//         return;
//       }

//       const fullJournalContent = fullJournal.root.innerHTML;
//       const fullAbstractContent = fullAbstract.root.innerHTML;

//       document.querySelector('input[name="fullJournalContent"]').value =
//         fullJournalContent;
//       document.querySelector('input[name="fullAbstractContent"]').value =
//         fullAbstractContent;
//       return;
//     });
//   });
// }

const imageUpload = document.querySelector("#image-upload");
const imageContainer = document.querySelector(".add-image");
const removeIcon = document.querySelector(".remove-image");
const emptyImageContainer = document.querySelector(".add-image-text");
if (addNewArticlePage !== null || addNewEventPage !== null) {
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
  // document.addEventListener("DOMContentLoaded", function () {
  //   const fullAbstract = new Quill("#full-abstract-editor", {
  //     modules: {
  //       toolbar: [
  //         ["bold", "italic", "underline"],
  //         ["link", "blockquote", "image"],
  //         [{ list: "ordered" }, { list: "bullet" }],
  //         [{ color: [] }, { background: [] }],
  //       ],
  //     },
  //     theme: "snow",
  //   });
  //   const form = document.getElementById("articleForm");
  //   form.addEventListener("submit", function (event) {
  //     if (fullAbstract.getText().trim() === "") {
  //       alert("Article body cannot be empty!");
  //       event.preventDefault();
  //       return;
  //     }

  //     const fullAbstractContent = fullAbstract.root.innerHTML;

  //     document.querySelector('input[name="fullAbstractContent"]').value =
  //       fullAbstractContent;
  //     return;
  //   });
  // });
}
