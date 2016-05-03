(function () {
  'use strict';

  /**
   * @ngdoc overview
   * @name horizon.app.core
   * @description
   *
   * # horizon.app.core
   *
   * This module hosts modules of core functionality and services that supports
   * components added to Horizon via its plugin mechanism.
   */
  angular
    .module('horizon.app.core', [
      'horizon.framework.conf',
      'horizon.framework.util',
      'horizon.framework.widgets',
    ], config);

  config.$inject = ['$provide', '$windowProvider'];

  function config($provide, $windowProvider) {
    var path = $windowProvider.$get().STATIC_URL + 'app/core/';
    $provide.constant('horizon.app.core.basePath', path);
  }

})();