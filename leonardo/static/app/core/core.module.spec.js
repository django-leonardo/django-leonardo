
(function () {
  'use strict';

  describe('horizon.app.core', function () {
    it('should be defined', function () {
      expect(angular.module('horizon.app.core')).toBeDefined();
    });
  });

  describe('horizon.app.core.basePath', function () {
    beforeEach(module('horizon.app.core'));

    it('should be defined and set correctly', inject([
      'horizon.app.core.basePath', '$window',
      function (basePath, $window) {
        expect(basePath).toBeDefined();
        expect(basePath).toBe($window.STATIC_URL + 'app/core/');
      }])
    );
  });

})();