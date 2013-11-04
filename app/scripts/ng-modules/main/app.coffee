'use strict'

App = angular.module('app', [
  'todo'
  'apartment'
  'search'
  'googleMaps'
  'main.controllers'
  'main.directives'
  'main.filters'
  'main.services'
  'partials'
  'stripe'
  'ngAnimate'
  'ui.router'
  'ui.bootstrap'
  'ui.utils'
])

App.config ($stateProvider, $urlRouterProvider) ->
  $urlRouterProvider.otherwise "/"

  $stateProvider.state "home",
    url: "/"
    templateUrl: "/_public/js/main/home.html"
    data:
      style:
        webAppStyle: false
  .state "styles",
      url: "/styles"
      templateUrl: "/_public/js/main/partial1.html"
  .state "search",
    url: "/search"
    templateUrl: "/_public/js/search/wizard/start.html"
    data:
      style:
        webAppStyle:true


App.config(($locationProvider) ->
  # Without server side support html5 must be disabled.
  $locationProvider.html5Mode(true)
)

App.config((RestangularProvider, AppConfig) ->
  RestangularProvider.setBaseUrl AppConfig.API_ENDPOINT
  RestangularProvider.setDefaultHttpFields
    withCredentials: true



  # This function is used to map the JSON data to something Restangular expects
  # http://stackoverflow.com/a/17386402/173957
  RestangularProvider.setResponseExtractor (response, operation, what, url) ->
    if operation == "getList"

      # Use results as the return type, and save the result metadata
      # in _resultmeta
      newResponse = response.results
      newResponse._resultMeta =
        count: response.count
        next: response.next
        previous: response.previous

      newResponse
    else
      response
)

# Declare app level module which depends on filters, and services
angular.module('main.controllers', [])
angular.module('main.directives', ['main.services'])
angular.module('main.filters', [])
angular.module('main.services', [])