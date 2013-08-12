# Filename: SidebarController.coffee

DashboardManager.module 'DashboardApp.Sidebar', (Sidebar, DashboardManager, Backbone, Marionette, $, _) ->
  Sidebar.Controller =
    listLinks: ->
      links = DashboardManager.request "link:entities"

      sidebarView = new Sidebar.Links
        collection: links

      DashboardManager.sidebar.show sidebarView

DashboardManager.module 'DashboardApp', (DashboardApp, DashboardManager, Backbone, Marionette, $, _) ->

  DashboardApp.Router = Backbone.Marionette.AppRouter.extend
    appRoutes:
      "overview": "listContacts"
      "": "listContacts"

  API =
    listContacts: ->
      console.log 'wow'

  DashboardManager.addInitializer -> new DashboardApp.Router
    controller: API

MyRouter = Backbone.Marionette.AppRouter.extend
  appRoutes:
    "dashboard#overview": "someMethod"

  routes :
    "aws-info" : "someOtherMethod"

  someOtherMethod: ->
    console.log 'boom'

  someMethod: ->
    console.log 'boom'

API =
  someOtherMethod: ->
    console.log 'boom'

  someMethod: ->
    console.log 'boom'
  listContacts: ->
    console.log 'wow'

myrouter = new MyRouter
  controller: API
