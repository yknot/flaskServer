function TasksViewModel() {
       var self = this;
       self.tasksURI = 'http://localhost:5000/api';
      // self.username = "miguel";
      //  self.password = "python";
       self.tasks = ko.observableArray();

       self.ajax = function(uri, method, data) {
           var request = {
               url: uri,
               type: method,
               contentType: "application/json",
               accepts: "application/json",
               cache: false,
               dataType: 'json',
               data: JSON.stringify(data),
              //  beforeSend: function (xhr) {
                  //  xhr.setRequestHeader("Authorization",
                      //  "Basic " + btoa(self.username + ":" + self.password));
              //  },
               error: function(jqXHR) {
                   console.log("ajax error " + jqXHR.status);
               }
           };
           return $.ajax(request);
       }

       self.ajax(self.tasksURI, 'GET').done(function(data) {
           for (var i = 0; i < data.tasks.length; i++) {
              console.log(data.tasks[i].title)
               self.tasks.push({
                   title: ko.observable(data.tasks[i].title),
                   description: ko.observable(data.tasks[i].description)
               });
           }
       });
   }
   ko.applyBindings(new TasksViewModel(), $('#main')[0]);
