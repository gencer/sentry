(function(){
  'use strict';

  app.models = {
    Group: Backbone.Model.extend({
      defaults: {
        count: 0,
        version: 0,
        annotations: [],
        tags: [],
        versions: [],
        hasSeen: false,
        isBookmarked: false,
        historicalData: []
      }
    })
  };
}());
