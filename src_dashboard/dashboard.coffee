# Filename: dashboard.coffee

DashboardManager.module 'Entities', (Entities, DashboardManager, Backbone, Marionette, $, _) ->

  Entities.Sidebar = Backbone.Model.extend {}
  Entities.SidebarCollection = Backbone.Collection.extend
    model: Entities.Sidebar

  links = new Entities.SidebarCollection(
    [
      id: 'overview'
      icon: 'icon-dashboard'
      name: 'Dashboard'
      url: '#overview'
    ,
      id: 'aws-info'
      icon: 'icon-lock'
      name: 'AWS Info'
      url: '#aws-info'
    ,
      id: 'database'
      icon: 'icon-table'
      name: 'Database'
      url: '#aws-info'
    ,
      id: 'server-params'
      icon: 'icon-cogs'
      name: 'Server'
      url: 'aws-info'
    ,
      id: 'hit-config'
      icon: 'icon-group'
      name: 'HIT Config'
      url: 'aws-info'
    ,
      id: 'expt-info'
      icon: 'icon-beaker'
      name: 'Expt Info'
      url: 'aws-info'
    ,
      id: 'pay-and-bonus'
      icon: 'icon-money'
      name: 'Pay'
      url: 'aws-info'
    ,
      id: 'sever-log'
      icon: 'icon-bug'
      name: 'Server Log'
      url: 'aws-info'
    ,
      id: 'documentation'
      icon: 'icon-question'
      name: 'Help'
      url: 'aws-info'
    ,
      id: 'contribute'
      icon: 'icon-github'
      name: 'Contribute'
      url: 'aws-info'
    ,
      id: 'Exit'
      icon: 'icon-power-off'
      name: 'Exit'
      url: 'aws-info'
    ])

  API =
    getLinkEntities: ->
      return links

  DashboardManager.reqres.setHandler "link:entities", ->
    return API.getLinkEntities()
