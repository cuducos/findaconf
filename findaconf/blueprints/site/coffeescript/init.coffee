$(document).ready ->

  $('#query').autocompleter {
    source: '/autocomplete/keywords',
    offset: 'results',
    highlightMatches: true
  }

  $('#location').autocompleter {
    source: '/autocomplete/places',
    offset: 'results',
    minLength: 4,
    highlightMatches: true
  }

  fix_lang_menu()
  fix_main_padding()

fix_lang_menu = ->
  lang_menu = $('li.lang').first()
  lang_submenu = $('ul', lang_menu).first()
  lang_menu_w = lang_menu.width()
  lang_submenu_w = lang_submenu.width()
  left_margin = lang_menu_w - (lang_submenu_w + 1)
  lang_submenu.css 'margin-left', left_margin + 'px'

fix_main_padding = ->
  footer_h = $('footer').height()
  $('main').css 'padding-bottom', (footer_h + 128) + 'px'