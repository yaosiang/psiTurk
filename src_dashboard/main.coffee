# Filename: main.coffee

# Require.js allows us to configure shortcut alias
require.config
  paths:
    jquery: "libs/jquery"
    underscore: "libs/underscore"
    backbone: "libs/backbone"
    text: "libs/text"
    cs: "libs/cs"
    bootstrap: "libs/bootstrap"
    dropdown: "libs/bootstrap-dropdown"
    collapse: "libs/bootstrap-collapse"
    tab: "libs/bootstrap-tab"
    nod: "libs/nod"
    bacon: "libs/Bacon"
    marionette : 'libs/backbone.marionette'

  # Shim sets the configuration for third party scripts that are not AMD compatible
  shim:
    # Twitter Bootstrap jQuery plugins
    bootstrap: ["jquery"]
    dropdown: ["bootstrap"]
    collapse: ["bootstrap"]
    tab: ["bootstrap"]
    nod: ["jquery"]
    backbone:
      deps: ["underscore", "jquery"]
      exports: "Backbone" #attaches "Backbone" to the window object
    underscore:
      exports: "_"
    marionette:
      deps : ['jquery', 'underscore', 'backbone']
      exports : 'Marionette'

# end shim
require [
  "jquery"
  "app"
  "bootstrap"
  "marionette"
  "dropdown"
  "collapse"
  "tab"
  "nod"
  "bacon"
  ],
  (
    $
    App
    Bootstrap
    Marionette
    dropdown
    tab
  ) ->
    App.initialize()
