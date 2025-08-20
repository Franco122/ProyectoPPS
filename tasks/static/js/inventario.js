const inventory = [];
let editIndex = null;

const inventoryTable = document.getElementById("inventoryTable");
const modal = document.getElementById("modal");
const addBtn = document.getElementById("addBtn");
const cancelBtn = document.getElementById("cancelBtn");
const inventoryForm = document.getElementById("inventoryForm");

const productInput = document.getElementById("product");
const categoryInput = document.getElementById("category");
const locationInput = document.getElementById("location");
const availableInput = document.getElementById("available");
const reservedInput = document.getElementById("reserved");
const onHandInput = document.getElementById("onHand");

function renderTable() {
  inventoryTable.innerHTML = "";
  inventory.forEach((item, index) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${item.product}</td>
      <td>${item.category}</td>
      <td>${item.location}</td>
      <td>${item.available}</td>
      <td>${item.reserved}</td>
      <td>${item.onHand}</td>
      <td class="actions">
        <button onclick="editItem(${index})">Edit</button>
        <button onclick="deleteItem(${index})">Delete</button>
      </td>
    `;

    inventoryTable.appendChild(row);
  });
}

function resetForm() {
  productInput.value = "";
  categoryInput.value = "";
  locationInput.value = "";
  availableInput.value = "";
  reservedInput.value = "";
  onHandInput.value = "";
  editIndex = null;
}

addBtn.onclick = () => {
  resetForm();
  modal.classList.remove("hidden");
  document.getElementById("modalTitle").innerText = "Add Inventory";
};

cancelBtn.onclick = () => {
  modal.classList.add("hidden");
};

inventoryForm.onsubmit = (e) => {
  e.preventDefault();

  const newItem = {
    product: productInput.value,
    category: categoryInput.value,
    location: locationInput.value,
    available: parseInt(availableInput.value),
    reserved: parseInt(reservedInput.value),
    onHand: parseInt(onHandInput.value),
  };

  if (editIndex !== null) {
    inventory[editIndex] = newItem;
  } else {
    inventory.push(newItem);
  }

  renderTable();
  modal.classList.add("hidden");
};

window.editItem = function(index) {
  const item = inventory[index];
  productInput.value = item.product;
  categoryInput.value = item.category;
  locationInput.value = item.location;
  availableInput.value = item.available;
  reservedInput.value = item.reserved;
  onHandInput.value = item.onHand;
  editIndex = index;
  document.getElementById("modalTitle").innerText = "Edit Inventory";
  modal.classList.remove("hidden");
};

window.deleteItem = function(index) {
  if (confirm("Are you sure you want to delete this item?")) {
    inventory.splice(index, 1);
    renderTable();
  }
};

renderTable();
