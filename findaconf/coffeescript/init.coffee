$(document).ready ->

  $('#query').autocompleter {
    source: '/autocomplete/keywords',
    highlightMatches: true
  }

  $('#location').autocompleter {
    source: '/autocomplete/googleplaces',
    minLength: 4,
    highlightMatches: true
  }

  $(window).resize -> fix_cover_height()

  set_tooltips()
  center_content()
  fix_cover_imgs()
  fix_lang_menu()

set_tooltips = ->
  $('.tooltipster').each ->
    content = $('span', $(this)).html()
    $(this).tooltipster { content: content, position: 'bottom', theme: 'tooltipster-findaconf' }

center_content = ->
  view_port = $(window).height()
  page = $('nav').innerHeight() + $('main').innerHeight() + $('footer').innerHeight()
  console.log view_port
  console.log page
  if page < view_port
    diff = view_port - page
    margin = Math.round(diff / 2)
    $('main').css 'padding', margin + 'px 0'

fix_lang_menu = ->
  lang_menu = $('li.lang').first()
  lang_submenu = $('ul', lang_menu).first()
  lang_menu_w = lang_menu.width()
  lang_submenu_w = lang_submenu.width()
  left_margin = lang_menu_w - (lang_submenu_w + 1)
  lang_submenu.css 'margin-left', left_margin + 'px'

fix_cover_imgs = ->
  $('img.cover').each ->
    img_url = $(this).attr 'src'
    parent = $(this).parent()
    css_value = "url('" + img_url + "')"
    parent.css 'background-image', css_value
    parent.html '&nbsp;'
    fix_cover_height parent.parent()
    $(this).hide()

fix_cover_height = (row=false) ->
  if !row
    row = $('div.result')
  row.each ->
    cover = $('div', $(this)).first()
    main = $('div:nth-child(2)', $(this)).first()
    height = main.height()
    cover.css 'height', height + 'px'