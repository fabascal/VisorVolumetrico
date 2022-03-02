var listView = document.querySelector(".list-view");
var gridView = document.querySelector(".grid-view");
var boxesGroups = document.querySelector(".boxes-groups");

listView.addEventListener("click", function () {
    gridView.classList.remove("active");
    listView.classList.add("active");
    boxesGroups.classList.remove("display-grid");
    boxesGroups.classList.add("display-list");
  });

gridView.addEventListener("click", function () {
    gridView.classList.add("active");
    listView.classList.remove("active");
    boxesGroups.classList.remove("display-list");
    boxesGroups.classList.add("display-grid");
});  


