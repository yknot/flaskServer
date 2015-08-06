// get url for use later
var getUrl = window.location;
var baseUrl = getUrl .protocol + "//" + getUrl.host + "/";

// function to make our api calls
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

// view model for task list
function TasksViewModel() {
   var self = this;
   // url for getting task list
   self.tasksURI = baseUrl + 'api';
   // create empty list of tasks
   self.tasks = ko.observableArray();

   // on selecting task navigate to page
   self.select = function(task) {
     window.location.href = task.title();
   }

   // get the list of tasks
   ajax(self.tasksURI, 'GET').done(function(data) {
       for (var i = 0; i < data.tasks.length; i++) {
           self.tasks.push({
               title: ko.observable(data.tasks[i].title),
               description: ko.observable(data.tasks[i].description)
           });
       }
  });
}

ko.applyBindings(new TasksViewModel());
