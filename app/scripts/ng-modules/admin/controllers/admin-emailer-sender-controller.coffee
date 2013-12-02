'use strict'

angular.module('admin.controllers')
.controller 'AdminEmailerSenderCtrl', ($scope, $state, AdminEmailerSenderModel, Restangular) ->
    $scope.settings =
      emailsPending: false

    Restangular.one('emailer_sender', $state.params.searchId).get().then (response) ->
      debugger
      $scope.model = response

    $scope.settings.sendEmails = ->
      $scope.settings.emailsPending = true
      $scope.model.post().then (->
        alert ('Sent')
      ), ->
        $scope.settings.emailsPending = false
        alert ('Error')
