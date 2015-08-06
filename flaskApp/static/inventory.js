// base url for later
var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host + "/";

// async api call
var ajax = function(uri, method, data) {
    var request = {
        url: uri,
        type: method,
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data),
        error: function(jqXHR) {
            console.log("ajax error " + jqXHR.status);
        }
    };
    return $.ajax(request);
}
// task view model
function TasksViewModel() {
   var self = this;
   self.tasksURI = baseUrl + 'api';
   self.tasks = ko.observableArray();

   ajax(self.tasksURI, 'GET').done(function(data) {
       for (var i = 0; i < data.tasks.length; i++) {
         // for skipping current task
        //  if(data.tasks[i].title == 'inventory'){
        //    continue;
        //  }
           self.tasks.push({
               title: ko.observable(data.tasks[i].title),
               description: ko.observable(data.tasks[i].description)
           });
       }
  });
}
// item view model
function ItemViewModel(inventory) {
  var self = this;

  // set inventory title
  self.title = inventory;
  // url for items
  self.itemsURI = baseUrl + 'api/inventory/' + inventory;

  // create array of items
  self.items = ko.observableArray();

  // dummy select functio for right now
  self.select = function(item) {
    alert("Selecting: " + item.item())
  }

  // get list of items and add them with all attributes
  ajax(self.itemsURI, 'GET').done(function(data) {
      for (var i = 0; i < data.items.length; i++) {
          self.items.push({
              item: ko.observable(data.items[i].name),
              id: ko.observable(data.items[i].id),
              expirationDate: ko.observable(data.items[i].expirationDate),
              purchaseDate: ko.observable(data.items[i].purchaseDate),
              purchasePrice: ko.observable(data.items[i].purchasePrice),
              quantity: ko.observable(data.items[i].quantity)
          });
      }
 });
}
// inventory view model
function InventoryViewModel() {
  var self = this;
  self.inventoriesURI = baseUrl + 'api/inventory';
  self.inventories = ko.observableArray();

  ajax(self.inventoriesURI, 'GET').done(function(data) {
      for (var i = 0; i < data.inventories.length; i++) {
          self.inventories.push(new ItemViewModel(data.inventories[i].name))
      }
 });
}

ko.applyBindings(new TasksViewModel(), $('.navbar')[0]);
ko.applyBindings(new InventoryViewModel(), $('#inv')[0]);
ko.applyBindings(new InventoryViewModel(), $('#items')[0]);
