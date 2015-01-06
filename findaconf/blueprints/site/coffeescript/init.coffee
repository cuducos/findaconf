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

  $('#flash a.close').click(sweet_hide)

  fix_lang_menu()

sweet_hide = ->
  alert_box = $(this).parent()
  properties = {
    height: 'toggle',
    marginBottom: 'toggle',
    marginTop: 'toogle',
    opacity: 'toggle',
    paddingBottom: 'toggle',
    paddingTop: 'toogle'
  }
  alert_box.animate properties, 'fast', check_flash

check_flash = ->
  flash_area = $('#flash')
  flash_area.slideUp() if $('li', flash_area).length?

fix_lang_menu = ->
  lang_menu = $('li.lang').first()
  lang_submenu = $('ul', lang_menu).first()
  lang_menu_w = lang_menu.width()
  lang_submenu_w = lang_submenu.width()
  left_margin = lang_menu_w - (lang_submenu_w + 1)
  lang_submenu.css 'margin-left', left_margin + 'px'
